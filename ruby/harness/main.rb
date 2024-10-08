require 'unleash'
require 'unleash/context'
require 'json'
require 'logger'

class NullLogger < Logger
  def initialize(*args)
  end

  def add(*args, &block)
  end
end

raw_data = $stdin.read
tests = JSON.parse(raw_data)["tests"]

logger = ENV['PUPPY_DEBUG'] == 'false' ? NullLogger.new : Logger.new(STDOUT)
unleash_api_url = ENV.fetch('UNLEASH_API_URL', 'http://localhost:4242/api/')

@unleash = Unleash::Client.new(
  url: unleash_api_url,
  custom_http_headers: { 'Authorization': 'SOME-SECRET' },
  app_name: 'bootstrap-test',
  instance_id: 'local-test-cli',
  refresh_interval: 1,
  logger: logger
)
client = Unleash::Client.new

output = {}
tests.each do |test|
  context = Unleash::Context.new test["context"]

  result = client.is_enabled?(test["toggleName"], context)

  output[test["description"]] = {
    "result" => result,
    "toggleName" => test["toggleName"],
  }
end

puts JSON.pretty_generate(output, indent: '    ')  # Silly hack to get Ruby to format with 4 spaces like literally every other language