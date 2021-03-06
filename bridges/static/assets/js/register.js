'use strict';
class Validator {
    constructor(form) {
        this.patterns = {
            name: /^[a-z]+$/i,
            phone: /^\+7\(\d{3}\)\d{3}-\d{2}-\d{2}$/,
            email: /^[\w._-]+@\w+\.[a-z]$/i,
        };
        this.errors = {
            name: 'Логин может содержать только латинские буквы',
            phone: 'Телефон должен подходить под шаблон +7(999)999-99-99'
        };
        this.errorClass = 'error-msg';
        this.form = form;
        this.valid = false;
        this._validateForm();
    }
    _validateForm(){
        let errors = [...document.getElementById(this.form).querySelectorAll(`.${this.errorClass}`)];
        for (let error of errors) {
            error.remove();
        }
        let formFields = [...document.getElementById(this.form).getElementsByTagName('input')];
        for (let field of formFields) {
            this._validate(field);
        }
        if(![...document.getElementById(this.form).querySelectorAll('.invalid').length]){
            this.valid = true;
        }
    }
    _validate(field) {
        if(this.patterns[field.name]) {
            if(!this.patterns[field.name].test(field.value)){
                field.classList.add('invalid');
                this._addErrorMsg(field);
                this._watchField(field);
            }
        }
    }
    _addErrorMsg(field){
        let error = `<div class="${this.errorClass}">${this.errors[field.name]}</div> `;
        field.parentNode.insertAdjacentHTML('beforeend', error);
    }
    _watchField(field){
        field.addEventListener('input', () => {
            let error = field.parentNode.querySelector(`.${this.errorClass}`);
            if(this.patterns[field.name].test(field.value)){
                field.classList.remove('invalid');
                field.classList.add('valid');
                if(error){
                    error.remove();
                }
            } else {
                field.classList.remove('valid');
                field.classList.add('invalid');
                if(!error){
                    this._addErrorMsg(field);
                }
            }
        });
    }
}
// Данные для передачи на сервер допустим id товаров и его количество
let userEmail;
let emailTag = document.getElementById('id_email');
if (emailTag) {
    emailTag.addEventListener('change', function () {
        userEmail = this.value;
        return new Promise((resolve) => {
            // Создаём объект класса XMLHttpRequest
            const request = new XMLHttpRequest();
            /*  Составляем строку запроса и кладем данные */
            const url = "check_email/?email=" + userEmail;
            /* Указываем параметры соединения с сервером, т.е. метод соединения и url-запрос. */
            request.open('GET', url);
            // Указываем заголовки для сервера, говорим что тип данных, - контент который мы хотим получить должен быть не закодирован.
            request.setRequestHeader('Content-Type', 'application/x-www-form-url');
            // Здесь мы получаем ответ от сервера на запрос, лучше сказать ждем ответ от сервера
            request.addEventListener("readystatechange", () => {
                /*   request.readyState - возвращает текущее состояние объекта XHR(XMLHttpRequest) объекта,
                бывает 4 состояния 4-е состояние запроса - операция полностью завершена, пришел ответ от сервера,
                вот то что нам нужно request.status это статус ответа,
                нам нужен код 200 это нормальный ответ сервера, 401 файл не найден, 500 сервер дал ошибку и прочее...   */
                if (request.readyState === 4 && request.responseText === 'ok') {
                    console.log(request.responseText);
                    resolve(this.setAttribute("style", "border: 2px solid royalblue; width: 500px;"));
                } else if (request.readyState === 4 && request.responseText === 'stay') {
                    console.log(request.responseText);
                    resolve(this.setAttribute('style', 'border: 1px solid #eaeaea; width: 500px;'));
                } else if (request.readyState === 4 && request.responseText === 'no') {
                    console.log(request.responseText);
                    resolve(this.setAttribute('style', 'border: 2px solid red; width: 500px;'));
                }
            });
            request.send()
        })
    });
}

let username;
let userTag = document.getElementById('id_username');
if (userTag) {
    userTag.addEventListener('blur', function () {
        username = this.value;
        return new Promise(resolve => {
            // Создаем объект класса XMLHttpRequest
            const request = new XMLHttpRequest();
            /* Создаём строку запроса и кладем данные */
            const url = "check_username/?username=" + username;
            /* Указываю параметры соединения с сервером то есть метод соединения и url-запрос */
            request.open('GET', url);
            /* Указываем заголовки для сервера, то есть тип данных для чтения и кодировка (а точнее её отсутствие) */
            request.setRequestHeader('Content-Type', 'application/x-www-form-url');
            /* Ждем ответ на запрос от сервера */
            request.addEventListener('readystatechange', () => {
                if (request.readyState === 4 && request.responseText === 'ok') {
                    console.log(request.responseText);
                    resolve(this.setAttribute("style", "border: 2px solid royalblue; width: 250px;"));
                } else if (request.readyState === 4 && request.responseText === 'stay') {
                    console.log(request.responseText);
                    resolve(this.setAttribute('style', 'border: 1px solid #eaeaea; width: 250px;'));
                } else if (request.readyState === 4 && request.responseText === 'no') {
                    console.log(request.responseText);
                    resolve(this.setAttribute('style', 'border: 2px solid red; width: 250px;'));
                }
            });
            request.send()
        });
    });
}

let userPhone;
let phoneTag = document.getElementById('id_phone');
if (phoneTag) {
    phoneTag.addEventListener('blur', function () {
        userPhone = this.value;
        return new Promise(resolve => {
            // Создаем объект класса XMLHttpRequest
            const request = new XMLHttpRequest();
            /* Создаем строку запроса и кладем в неё данные */
            const url = 'check_phone/?phone=' + userPhone;
            /* Указываю тип соединения с сервером и сам url-запрос */
            request.open('GET', url);
            /* Указываю заголовок для сервера чтобы донести ло него тип данных и их кодировку (а точнее её отсутствие) */
            request.setRequestHeader('Content-Type', 'application/x-www-form-url');
            /* Ждем ответ на запрос от сервера */
            request.addEventListener('readystatechange', () => {
                if (request.readyState === 4 && request.responseText === 'ok') {
                    console.log(request.responseText);
                    resolve(this.setAttribute("style", "border: 2px solid royalblue; width: 250px;"));
                } else if (request.readyState === 4 && request.responseText === 'stay') {
                    console.log(request.responseText);
                    resolve(this.setAttribute('style', 'border: 1px solid #eaeaea; width: 250px;'));
                } else if (request.readyState === 4 && request.responseText === 'no') {
                    console.log(request.responseText);
                    resolve(this.setAttribute('style', 'border: 2px solid red; width: 250px;'));
                }
            });
            request.send()
        });
    });
}
