from django.db import models

DIFFICULTY_CHOICES = {
    1: 'Низкая',
    2: 'Ниже',
    3: 'Средняя',
    4: 'Выше',
    5: 'Высокая',
}

LESSON_PART_TYPES = {
    'TEST': 'Тест',
    'LECTURE': 'Лекция',
}


class Lesson(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название урока')
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, verbose_name='Сложность')
    creator = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Создатель',
        related_name='created_lessons',
    )
    dt_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания урока')
    dt_updated = models.DateTimeField(auto_now=True, verbose_name='Дата и время редактирования урока')
    listeners = models.ManyToManyField(
        'auth.User',
        verbose_name='Слушатели',
        related_name='opened_lessons',
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class LessonPart(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название части урока')
    lesson = models.ForeignKey('education.Lesson', on_delete=models.SET_NULL, null=True, verbose_name='Урок')
    number = models.IntegerField(verbose_name='Порядковый номер')
    content = models.CharField(max_length=5000, verbose_name='Контент части урока', blank=True)
    type = models.CharField(choices=LESSON_PART_TYPES, max_length=7, verbose_name='Тип части урока')
    dt_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания части урока')
    dt_updated = models.DateTimeField(auto_now=True, verbose_name='Дата и время редактирования части урока')

    class Meta:
        verbose_name = 'Часть урока'
        verbose_name_plural = 'Части уроков'
        unique_together = ('lesson', 'number')


class TestPart(models.Model):
    lesson_part = models.ForeignKey('education.LessonPart', on_delete=models.CASCADE, verbose_name='Часть урока')
    content = models.CharField(max_length=100, verbose_name='Контент вопроса теста')
    number = models.IntegerField(verbose_name='Порядковый номер')

    class Meta:
        verbose_name = 'Часть теста'
        verbose_name_plural = 'Части теста'
        unique_together = ('lesson_part', 'content',)


class Answer(models.Model):
    test_part = models.ForeignKey('education.TestPart', on_delete=models.CASCADE, verbose_name='Часть теста')
    content = models.CharField(max_length=100, verbose_name='Контент вопроса ответа')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ')

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'
        unique_together = ('test_part', 'content', )
