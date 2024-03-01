require 'unleash'
require 'unleash/context'
require 'logger'


class NullLogger < Logger
  def initialize(*args)
  end

  def add(*args, &block)
  end
end

puts "poc-ruby"
@unleash = Unleash::Client.new(
  url: 'https://empty/api',
  custom_http_headers: { 'Authorization': 'empty' },
  app_name: 'bootstrap-test',
  instance_id: 'local-test-cli',
  refresh_interval: 2,
  disable_client: true,
  disable_metrics: true,
  metrics_interval: 2,
  retry_limit: 2,
  logger: NullLogger.new,
  bootstrap_config: Unleash::Bootstrap::Configuration.new(file_path: "feature_toggles.json")
)

client = Unleash::Client.new

context = Unleash::Context.new

feature_name = "featureX"
if client.is_enabled?(feature_name, context)
  puts "Feature enabled"
else
  puts "Feature '#{feature_name}' is not enabled."
end
