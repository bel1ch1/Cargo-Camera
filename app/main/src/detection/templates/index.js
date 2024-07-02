
document.addEventListener('DOMContentLoaded', function() {
    // Получаем форму по её ID
    var size_form = document.getElementById('set_size_form');

    // Добавляем обработчик события отправки формы
    size_form.addEventListener('submit', function(event) {
         // Предотвращаем стандартное поведение формы
        event.preventDefault();

        // Получаем значение из поля ввода
        var size = size_form.size.value;

        // Создаем объект XMLHttpRequest
        var xhr = new XMLHttpRequest();

        // Отправляем запрос к API
        xhr.open('POST', '/set_marker_size?size=' + encodeURIComponent(size), true);

        // Добавляем обработчик события на успешное завершение запроса
        xhr.onload = function() {
            if (xhr.status === 200) {
                // Выводим ответ от сервера
                console.log(xhr.responseText);
            } else {
                // Обработка ошибок
                console.error('Request failed');
            }
        };

        // Отправляем запрос
        xhr.send();
    });
});
