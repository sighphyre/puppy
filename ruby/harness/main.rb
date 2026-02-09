require 'unleash'
require 'unleash/context'
require 'unleash/variant'
require 'json'
require 'logger'
require 'net/http'
require 'uri'

INITIAL_FETCH_TIMEOUT_MS = 2000

class NullLogger < Logger
  def initialize(*args)
  end

  def add(*args, &block)
  end
end

logger = ENV['PUPPY_DEBUG'] == 'false' ? NullLogger.new : Logger.new(STDOUT)
unleash_api_url = ENV.fetch('UNLEASH_API_URL', 'http://localhost:4242/api/')
unleash_api_key = ENV.fetch('UNLEASH_API_KEY', 'SOME-SECRET')
run_id = ENV.fetch('PUPPY_RUN_ID', 'default')
puppy_base_url = ENV.fetch('PUPPY_BASE_URL', 'http://localhost:4242')
tests_url = "#{puppy_base_url}/api/tests"
report_url = "#{puppy_base_url}/api/report/ingest"
input = {}

begin
  uri = URI.parse(tests_url)
  input = JSON.parse(Net::HTTP.get(uri))
rescue StandardError => e
  raise "Failed to fetch tests from #{tests_url}: #{e.class} #{e}"
end

tests = input["tests"] || []

@unleash = Unleash::Client.new(
  url: unleash_api_url,
  custom_http_headers: { 'Authorization': unleash_api_key },
  app_name: 'bootstrap-test',
  instance_id: 'local-test-cli',
  refresh_interval: 1,
  logger: logger
)
client = @unleash

def wait_for_initial_fetch(timeout_ms)
  fetcher = Unleash.toggle_fetcher
  return if fetcher.nil?

  deadline = Time.now + (timeout_ms / 1000.0)
  fetcher.toggle_lock.synchronize do
    while fetcher.etag.nil? && Time.now < deadline
      remaining = deadline - Time.now
      break if remaining <= 0
      fetcher.toggle_resource.wait(fetcher.toggle_lock, remaining)
    end
  end
end

wait_for_initial_fetch(INITIAL_FETCH_TIMEOUT_MS)

results = []
tests.each do |test|
  test_id = test["id"] || test["name"] || "unknown"
  steps = test["steps"] || []

  steps.each_with_index do |step, index|
    op = step["op"]
    toggle_name = step["toggleName"]
    context = Unleash::Context.new(step["context"])

    case op
    when "isEnabled"
      raise "Missing toggleName for isEnabled step" if toggle_name.nil?
      default_value = step.key?("defaultValue") ? step["defaultValue"] : false
      result = client.is_enabled?(toggle_name, context, default_value)
      results << {
        "testId" => test_id,
        "stepIndex" => index,
        "op" => op,
        "toggleName" => toggle_name,
        "result" => result,
      }
    when "getVariant"
      raise "Missing toggleName for getVariant step" if toggle_name.nil?
      default_variant_input = step["defaultVariant"]
      fallback_variant = if default_variant_input
                           Unleash::Variant.new(default_variant_input)
                         else
                           Unleash::Variant.disabled_variant
                         end
      variant = client.get_variant(toggle_name, context, fallback_variant)
      results << {
        "testId" => test_id,
        "stepIndex" => index,
        "op" => op,
        "toggleName" => toggle_name,
        "result" => {
          "name" => variant.name,
          "enabled" => variant.enabled,
          "payload" => variant.payload,
        },
      }
    else
      raise "Unknown op: #{op}"
    end
  end
end

report_payload = {
  "meta" => {
    "sdk" => "ruby",
    "runId" => run_id,
  },
  "results" => results
}

if report_url
  uri = URI.parse(report_url)
  http = Net::HTTP.new(uri.host, uri.port)
  request = Net::HTTP::Post.new(uri.request_uri)
  request["Content-Type"] = "application/json"
  request["X-Run-Id"] = run_id
  request.body = JSON.generate(report_payload)
  http.request(request)
end

puts "Closed test run with runId=#{run_id}, sent #{results.size} results to #{report_url}"

client.shutdown
