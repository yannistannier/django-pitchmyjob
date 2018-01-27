from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from apps.authentication.models import User
from apps.data.models import Industry, Employee, ContractType, Experience, StudyLevel


from ._data import INDUSTRIES, EMPLOYEES, CONTRACT_TYPES, EXPERIENCES, STUDY_LEVELS, GROUPS, ADMINS


class Command(BaseCommand):
    help = 'Initializes the database with basic data'

    industries = INDUSTRIES
    employees = EMPLOYEES
    contract_types = CONTRACT_TYPES
    experiences = EXPERIENCES
    study_levels = STUDY_LEVELS
    groups = GROUPS
    admins = ADMINS

    def handle(self, *args, **options):
        self.stdout.write('# init_data command start')
        self.add_general_data(Industry, 'industries')
        self.add_general_data(Employee, 'employees')
        self.add_general_data(ContractType, 'contract_types')
        self.add_general_data(Experience, 'experiences')
        self.add_general_data(StudyLevel, 'study_levels')
        self.add_groups()
        self.add_admins()
        self.stdout.write('\n# init_data command end')

    def add_groups(self):
        self.stdout.write('\n>> Add groups')

        groups = getattr(self, 'groups', None)
        if groups:
            for group in groups:
                name = group.get('name')
                obj, created = Group.objects.get_or_create(name=name)
                if created:
                    message = '"{}" has been created with id {}'.format(name, obj.pk)
                    self.stdout.write(self.style.SUCCESS(message))
                else:
                    message = '"{}" already exists with id {}'.format(name, obj.pk)
                    self.stdout.write(self.style.WARNING(message))

                permissions = group.get('permissions')
                if permissions:
                    for permission in permissions:
                        app_label = permission.get('app_label')
                        model_name = permission.get('model')
                        codenames = permission.get('codenames')

                        content_type = ContentType.objects.get(app_label=app_label, model=model_name)
                        perms = Permission.objects.filter(content_type=content_type, codename__in=codenames)
                        for perm in perms:
                            message = '\t"{}" has been added to group'.format(perm.codename)
                            self.stdout.write(self.style.SUCCESS(message))
                            obj.permissions.add(perm)
        else:
            self.stderr.write('No data to deal with')

    def add_admins(self):
        self.stdout.write('\n>> Add admins')

        admins = getattr(self, 'admins', None)
        if admins:
            for admin in admins:
                email = admin.get('email')
                obj = User.objects.filter(email=email).first()
                if not obj:
                    obj = User.objects.create_superuser(**admin)
                    message = '"{}" has been created with id {}'.format(email, obj.pk)
                    self.stdout.write(self.style.SUCCESS(message))
                else:
                    message = '"{}" already exists with id {}'.format(email, obj.pk)
                    self.stdout.write(self.style.WARNING(message))
        else:
            self.stderr.write('No data to deal with')

    def add_general_data(self, model, var_name):
        self.stdout.write('\n>> Add "{}" data'.format(model.__name__))

        names = getattr(self, var_name, None)
        if names:
            order = 10
            for name in names:
                obj, created = model.objects.get_or_create(name=name, defaults={'order': order})
                if created:
                    message = '"{}" has been created with order {} and id {}'.format(name, order, obj.pk)
                    self.stdout.write(self.style.SUCCESS(message))
                else:
                    message = '"{}" already exists with order {} and id {}'.format(name, obj.order, obj.pk)
                    self.stdout.write(self.style.WARNING(message))
                order += 10
        else:
            self.stderr.write('No data to deal with')
