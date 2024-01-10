from django.core.management.base import BaseCommand, CommandError
from NewsPaper.news.models import Post, Category


class Command(BaseCommand):
    help = 'Удаление всех постов из какой либо категории'
    missing_args_message = 'Предоставьте аргументы'

    def add_arguments(self, parser):
        parser.add_argument('argument', nargs='+', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все посты из категории {options["category"]}? yes/no')
        if answer != 'yes':
            self.stdout.write(self.stile.ERROR('Отменино'))
            return
        try:
            category = Category.objects.get(name=options["category"])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Все посты успешно удалены из категории {category.name_of_category}'))
        except Post.DoesNotExist:
            self.stdout.write(self.stile.ERROR(f'Нужно найти категорию'))
