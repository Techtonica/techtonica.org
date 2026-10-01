Rails.application.routes.draw do
  # ... outras rotas ...
  
  namespace :admin do
    get 'dashboard', to: 'dashboard#index'
    resources :applications, only: [:index, :show, :edit, :update]
    post 'applications/:id/notes', to: 'applications#create_note', as: :add_note
    post 'applications/:id/message', to: 'applications#send_message', as: :send_message
  end
end
