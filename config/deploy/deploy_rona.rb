server '158.69.79.94', user: 'deploy', roles: %w{web} ##, my_property: :my_value
# server '54.208.83.36', user: 'deploy', roles: %w{web}

set :ssh_options, {
   keys: %w(/Users/20/.ssh/server_id_rsa),
   forward_agent: false
 }
