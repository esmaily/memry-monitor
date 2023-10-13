# Python Monitor Memory Usage

> This project a good example implements python memory usage.

### Licensing

The project operates under the MIT license, which not only facilitates its use in commercial and open-source projects
but also encourages further development and sharing within the community.

### Setting Up the Project


##### Supporting report data:

- `async`
- `sync`

#### 1. Create  environment:

```sh
$ python -m venv myvenv
$ source myvenv/bin/activate
```

#### 2. Install  requirements:

```sh
$ pip install -r requirements.txt
```

#### 3. Run monitor memory usage:

```sh
$ python monitor.py

```

#### 4. Now run fastapi for reports:

> please attention you can run `async` or `synce` fastapi for report data

```sh
$ uvicorn async_main:app --host 0.0.0.0 --reload
```

> or run sync normal

```sh
$ uvicorn main:app --host 0.0.0.0--reload
```

#### 5. Get reports :

```sh
$ curl -X GET 127.0.0.1:8000/memory-reports
```

#### 6. Run Test :

```sh
$ pytest
```

### Project link

1. [Project root path](http://127.0.0.1:8000/)
2. [Swagger ui](http://127.0.0.1:8000/docs/)
3. [Report data](http://127.0.0.1:8000/memory-reports/)



 