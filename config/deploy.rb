lock '3.5.0'

set :application, 'fairbnb'                                ## application name
set :repo_url, 'git@github.com:ronachong/airbnb_clone.git' ## application repo
set :branch, 'master'
set :scm, :git                                             ## software configuration mgmt


set :deploy_to, '/home/deploy/fairbnb'                         ## dir to deploy to
set :tmp_dir, '/home/deploy/tmp'

set :stages, ["deploy_rona", "deploy_william"]             ## one stage each for deploying to Rona's servers & William's servers
set :default_stage, "deploy_rona"                          ## default stage to deploy to




namespace :deploy do

  after :restart, :clear_cache do
    on roles(:web), in: :groups, limit: 3, wait: 10 do
      # Here we can do anything such as:
      # within release_path do
      #   execute :rake, 'cache:clear'
      # end
    end
  end

end
