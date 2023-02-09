from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()

def test_get_api_key_valid_user(email=valid_email, password=valid_password):
    """Проверяем что код статуса запроса 200 и в переменной result содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """Проверяем что запрос всех питомцев возвращает не пустой список.
     Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name="Дуся", animal_type="дворняга", age="8",
                                               pet_photo="images/dvor.jpg"):
    """Проверяем добавление питомца с корректными данными и фото"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_and_photo(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

   # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_and_photo(auth_key, 'Zum', 'Dog', '2', 'images/Tibetski.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pets(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Афина', animal_type='Тибетский мастиф', age='1'):
    """Проверяем возможность изменения данных питомца"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Питомцы отсутствуют")
    # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев

"""ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ"""

#Позитивные тесты

def test_add_pets_with_valid_data_without_photo(name='Спок', animal_type='кот', age='11'):
    """Проверяем возможность добавления нового питомца без фото"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200
    assert result['name'] == name

def test_add_photo_at_pet(pet_photo='images/cat.jpg'):
    """Проверяем возможность изменения фото последнего созданного питомца"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        # Берем последнего добавленного питомца и меняем его фото
        status, result = pf.post_add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200
        assert result['pet_photo'] != ''

    else:
        raise Exception("Питомцы отсутствуют")

def test_on_delete_all_pets():
    """Проверяем удаление всех питомцев"""
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_and_photo(auth_key, 'Zum', 'Dog', '2', 'images/Tibetski.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Сохраняем id первого питомца в списке:
    pet_id = my_pets['pets'][0]['id']
    # Получаем в цикле id всех питомцев из списка и отправляем запрос на удаление:
    for id_pet in my_pets["pets"]:
        pf.delete_pets(auth_key, id_pet["id"])
    # Ещё раз запрашиваем список своих питомцев
    status, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()

# Негативные тесты:

def test_get_api_key_with_wrong_password_and_correct_mail(email=valid_email, password=invalid_password):
    """Проверяем запрос с невалидным паролем и с валидным емейлом. Проверяем нет ли ключа в ответе"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_api_key_with_wrong_email_and_correct_password(email=invalid_email, password=valid_password):
    """Проверяем запрос с невалидным емейлом и валидным паролем.Проверяем нет ли ключа в ответе"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_api_key_for_non_mail_and_pass(email='', password=''):
    """Проверяем что запрос api ключа возвращает статус 403. Если нет email и password """

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "key" is not result

def test_add_pet_negative_age_number(name='Умка', animal_type='белый медведь', age='-5'):
    """Проверка добавления питомца с отрицательным числом в переменной age.
    Тест не будет пройден если питомец будет добавлен на сайт с отрицательным числом в поле возраст"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца и сверяем полученный ответ с ожидаемым результатом
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    if int(age) > 0:
        # сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
    else:
        # если питомец добавлен с отрицательным числом, то выкидываем исключение
        raise Exception("Питомец добавлен на сайт с отрицательным числом в поле возраст")

def test_add_pet_with_four_digit_age_number(name='Timoha', animal_type='cat', age='51'):
    """Проверка добавления питомца с числом более 30 в переменной age.
    Тест не будет пройден если питомец будет добавлен на сайт с числом превышающим 30 в поле возраст"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    number = result['age']

    if int(age) <= 30:
        # сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
    else:
        # если питомец добавлен с числом >=30, то выкидываем исключение
        raise Exception("Питомец добавлен на сайт с числом привышающим 30")

def test_add_new_pet_with_missing_name (name='', animal_type='двортерьер', age='3'):
    """Проверка добавления питомца с пустым значением в переменной имя.
    Тест не будет пройден если питомец будет добавлен на сайт с пустым полем имя"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    if len(name) !=0:
    # сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
    else:
        # если питомец добавлен с пустым именем, то выкидываем исключение
        raise Exception("Питомец добавлен на сайт с пустым значением в имени")

def test_delete_self_pet_without_id():
    """Проверяем код по удалению питомца без указания id."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_and_photo(auth_key, 'Zum', 'Dog', '2', 'images/Tibetski.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = ""
    status, _ = pf.delete_pets(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 404 и в списке питомцев нет id удалённого питомца
    print('\n', "pet_id::", pet_id)
    assert status == 404
    assert pet_id not in my_pets.values()
