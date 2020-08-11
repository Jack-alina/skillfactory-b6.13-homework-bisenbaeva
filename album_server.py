from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album

@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        album_count = album.album_counter(artist)
        result = "<h1>" + "Количество альбомов {} - ".format(artist) + str(album_count) + "</h1>"
        result += "<h2>" + "Список альбомов {}:<br>".format(artist) + "</h2>"
        result += "<p>" + "<br>".join(album_names) + "</p>"
    return result

@route("/albums", method="POST")
def getNewAlbum():
    year = request.forms.get("year")
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album_name = request.forms.get("album")

    if (year != None) & (artist != None) & (genre != None) & (album_name != None): 
    # В  этом if проверяем все ли данные передал пользователь в POST-запросе
    # Если не все, то выдаем соответствующее сообщение
        try: 
            int(year)
            # В этом try пытаемся преобразовать year, который имеет тип string, в integer, чтобы убедиться, что пользователь ввел именно год, то есть целое число
            # Если нет, выдаем соответсвующее сообщение в except
        except:
            message = "Введен некорректный год"
            return HTTPError(400, message)
        else:
            new_album = album.add_album(year, artist, genre, album_name)

            if not new_album:
                return "Альбом успешно добавлен в базу данных, Спасибо!"
            else:
                message = "Альбом {} уже есть в базе данных".format(album)
                return HTTPError(409, message)
    else:
        message = "Не все необходимые параметры переданы в запросе"
        return HTTPError(400, message) 

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)