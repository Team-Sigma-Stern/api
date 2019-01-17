# API
This is the Backend of the online Texteditor
## Start
``` s
env FLASK_APP=main.py flask run -h 0.0.0.0 -p 5090090
```
## Folders
<p style="color:red;">To be Fix ed</p>
`./global` # **root** Only for development, in production probaly some where in /usr/share

`|-Projects` **project** Folder

`|-/$projectname`

## Api calls
### Paths
`/` <br>
`/login` **POST**: Login User. request body: `{ "name":...",password:"..." }` answer body:`{ "name":"...", "display-name":"...","auth-token":"..."}` <br>
`/logout` **POST** <br>
`/projects` **GET**: List projects 

`/projects/<project name>`<br>
`/projects/<project name>/files` **GET**: List Files <br>
`/projects/<project name>/files/<file name>` **GET**: Gets the content of `<file name>` **POST**: Sets the content of `<file name>`. If the file allready exists, it's need to be locked **DELETE** Deletes files, needs to be locked<br>
`/projects/<project name>/files/<file name>/lock` **GET**: Is the file locked response:`{"locked":"You | Other | No "}`  **POST**: Locks the file <br>
`/projects/<project name>/files/<file name>/unlock` **POST**: unlocks the file

### Header
    *"auth-token" the token used for authentification

### Codes
http codes used by the API
| Code | Case                                                                     | Response       |
| ---- | ------------------------------------------------------------------------ | -------------- |
| 200  | Get Succesfull                                                           | standard       |
| 201  | POST Succesfull                                                          | standard       |
| 204  | Get Request to /                                                         | none           |
| 400  | User Request couldnt processed successfully                              | Error response |
| 401  | No auth-token provided and request forbbiden for public or token expired | none           |
| 403  | The file, the client tryed ti write to, was not locked                   | none           |
| 404  | Resources not existing or The authentified user has no acces rights      | none           |
| 501  | This feature is not implemented, but will be                             | none           |

###Error response

Will be the response if an Error occured

`{`<br>
`"message":".."` should be shown to the user<br>
`}`

## Roles
**admin** can change project <br>
**user** can change files <br>
**guest** can view files



