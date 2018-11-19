from routes import Route

Route.get('/', 'IndexController@index')
Route.get('/test', 'IndexController@test')