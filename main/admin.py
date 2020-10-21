from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Language)
admin.site.register(Batch)
admin.site.register(Student)
admin.site.register(Assignment)
admin.site.register(Solution)
admin.site.register(Topic)
admin.site.register(Testcase)
admin.site.register(TestcaseOutput)
admin.site.register(SampleTestCase)
admin.site.register(Grade)
admin.site.register(TemporarySaveAssignmentData)
