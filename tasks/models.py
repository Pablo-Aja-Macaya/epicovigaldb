from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=50)
    urls = models.TextField() # escribir posibles urls separadas por ;
    buttons = models.TextField() # escribir posibles botones separados por ;
    image = models.ImageField(upload_to='images/')
    body = models.TextField(max_length=300)
    
    def __str__(self):
        return self.title
    def summary(self):
        return self.body[:80]
    def url_list(self):
        return self.urls.split(';')
    # def button_list(self):
    #     return self.buttons.split(';')
    def url_button_dict(self):
        url_list = self.urls.split(';')
        button_list = self.buttons.split(';')
        dictionary = {}
        for i in range(len(url_list)):
            dictionary[url_list[i]] = button_list[i]
        return dictionary



    