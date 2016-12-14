from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from .utils import make_previews_img_models

# Create your models here.
class Task(models.Model):
    task_text = models.TextField()
    title = models.CharField(max_length=200, blank=True)
    pub_date = models.DateTimeField('date published')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class TaskForm(ModelForm):
	class Meta:
		model = Task
		fields = ['title','task_text']
		template_name = 'tasks/task_new.html'

class Images (models.Model):
    # ...
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='image/original/', null=True, blank=True)
    task = models.ForeignKey('Task', on_delete=models.CASCADE,default=1)

    def save(self):
        try:
            img_obj = ImageModels.objects.get(id=self.id)
        except:
            img_obj = None
        super(Images,self).save()
        if not img_obj or img_obj.image != self.image:
            make_previews_img_models(self, None)


    def generate_path(instance, filename):
        ext = filename.rsplit('.', 1)[-1]
        h = md5(instance.user.username.encode()).hexdigest()
        result = 'photos/%s/%s/%s.%s' % (h[:2], h[2:4], h[4:], ext)
        path = os.path.join(settings.MEDIA_ROOT, result)
        if os.path.exists(path):
            os.remove(path)
        return result

class ImagesForm(ModelForm):
	class Meta:
		model = Images
		fields = ['title','image']
		template_name = 'tasks/image_new.html'
