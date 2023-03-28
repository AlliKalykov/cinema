from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название') # Название
    long_time = models.IntegerField(verbose_name='Длительность', help_text='В минутах') # Длительность
    start_date = models.DateField(verbose_name='Дата выхода') # Дата выхода
    end_date = models.DateField(verbose_name='Дата окончания') # Дата окончания
    company = models.CharField(max_length=100, verbose_name='Прокатчик') # Компания

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        ordering = ['start_date']


class Room(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название') # Название
    capacity = models.IntegerField(verbose_name='Вместимость') # Вместимость
    description = models.TextField(verbose_name='Описание') # Описание
    row_count = models.IntegerField(verbose_name='Количество рядов') # Количество рядов
    seat_count = models.IntegerField(verbose_name='Количество мест') # Количество мест

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Зал'
        verbose_name_plural = 'Залы'
        ordering = ['name']


class Job(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название') # Название

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        ordering = ['name']


class Employee(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя') # Имя
    surname = models.CharField(max_length=100, verbose_name='Фамилия') # Фамилия
    patronymic = models.CharField(max_length=100, verbose_name='Отчество') # Отчество
    position = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name='Должность') # Должность
    password = models.CharField(max_length=100, verbose_name='Пароль') # Пароль

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['name']


class Seat(models.Model):
    row = models.IntegerField(verbose_name='Ряд') # Ряд
    number = models.IntegerField(verbose_name='Номер') # Номер
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Зал') # Зал

    def __str__(self):
        return f'Ряд: {self.row}\nМесто: {self.number}'
    
    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'
        ordering = ['row', 'number']


class Sector(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название') # Название
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Зал') # Зал
    description = models.TextField(verbose_name='Описание') # Описание

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Сектор'
        verbose_name_plural = 'Секторы'
        ordering = ['name']


class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм') # Фильм
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Зал') # Зал
    start_date = models.DateTimeField(verbose_name='Дата начала') # Дата начала

    def __str__(self):
        return f'{self.movie.name} - {self.start_date}'
    
    class Meta:
        verbose_name = 'Сеанс'
        verbose_name_plural = 'Сеансы'
        ordering = ['start_date']


class TicketPrice(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название') # Название
    price = models.IntegerField(verbose_name='Цена') # Цена
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name='Сеанс') # Сеанс
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, verbose_name='Сектор') # Сектор

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Цена билета'
        verbose_name_plural = 'Цены билетов'
        ordering = ['name']


class Ticket(models.Model):
    STATUS_CHOICES = (
        ('empty', 'Свободен'),
        ('reserved', 'Забронирован'),
        ('sold', 'Продан'),
        ('destroyed', 'Уничтожен'),
    )
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name='Сеанс') # Сеанс
    price = models.ForeignKey(TicketPrice, on_delete=models.CASCADE, verbose_name='Цена') # Цена
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, verbose_name='Место') # Место
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания') # Дата создания
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='empty', verbose_name='Статус') # Статус


    def __str__(self):
        return f'{self.session.movie.name} - {self.price.price} - {self.seat}'
    
    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'
        ordering = ['session', 'price', 'seat']


class MovingTicket(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name='Билет') # Билет
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания') # Дата создания
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Сотрудник') # Сотрудник
    operation = models.CharField(max_length=100, verbose_name='Операция') # Операция

    def __str__(self):
        return f'{self.ticket} - {self.operation}'
    
    class Meta:
        verbose_name = 'Движение билета'
        verbose_name_plural = 'Движения билетов'
        ordering = ['ticket', 'created_at']
