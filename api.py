import json.decoder
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:
    """АPI библиотека к приложению PetFriends"""

    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru'

    def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус и результат в формате JSON с уникальным ключом
        пользователя, найденного по введеным емайл и паролю"""

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + '/api/key', headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return  status, result

    def get_list_of_pets(self, auth_key: json, filter: str) -> json:
        """Метод делает запрос и возвращает стас запроса и результат в формате JSON со списком найденных питомцев
        в соответсвии с фильтром. На данный момент список может иметь пустое значение - получить список всех животных,
        либо "my_pets" - получить список собственных питомцев"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + '/api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return  status, result

    def post_add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """Метод отправляет(постит) на сервeр данные о новом питомце (имя, пароду, возраст, фото) и возврващает статус запроса
         на сервер и результат в формате JSON с данными добавленного питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'images/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + '/api/pets', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def delete_pet_from_database(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет запрос на сервер для удаления питомца по указанному ID с базы данных,
        возвращает результат и статус кода в формате JSON с текстом об успешном удалении.
        На сегоднешний день тут баг, в result  приходит пустая строка, при этом статус код 200"""

        headers = {"auth_key": auth_key['key']}

        res = requests.delete(self.base_url + '/api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_information_about_pet(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: str) -> json:
        """Метод отправляет запрос на сервер на обновление информации о питомце
        возвращает статус код 200 и результат в формате JSON с обновленными данными о питомце"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        res = requests.put(self.base_url + '/api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_create_pet_simple(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """Метод отправляет (постит) на API сервер данные о новом питомце (имя, парода, возраст, без фото)
        и возвращает статус запроса и  результат в формате JSON с данными о новом питомце"""

        headers = { 'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        res = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_add_photo_of_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод отправляет запрос на сервер на добавление фотографии к существующему питомцу по id и
        возвращает статус запроса на сервер и результат в формате JSON с текстом об успешном дабавлении фото"""

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open('pet_photo', 'rb'), 'images/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content_type': data.content_type}

        res = requests.post(self.base_url + '/api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

































