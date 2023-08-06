Erscimenu
=========
Create UL LI html menu from django model queryset .
into your ``views`` or your ``template``.

Quick start
-----------

 Add ``erscimenu`` to your INSTALLED_APPS setting like this:
``INSTALLED_APPS = [
...,
'erscimenu' ,
]``

2.(Optional) Register ``Ulmenu`` to admin like this:

``from erscimenu.models import Ulmenu``

``admin.site.register(Ulmenu)`` 

and add your menu into it.

3.Run ``python manage.py makemigrations`` and ``python manage.py migrate``  to create the Ulmenu models.

4.Use this command to add menu with your views:

``from erscimenu.menu import MenuClass``

``from erscimenu.models import Ulmenu``

``cl = MenuClass()``

``clmenu = cl.ulmenu(Ulmenu.objects.all(),None)``

``return render(request,"index.html",{'model' : model })``

Note :  'model' is variable to use in your template.

Or create your model like this:

class Ulmenu(models.Model):

	title = models.CharField(max_length=100)

	css_class = models.CharField(max_length=100,null=True,blank=True)

	link = models.CharField(max_length=1000,null=True,blank=True)

	parent = models.ForeignKey("self", models.DO_NOTHING,null=True,blank=True,db_column='parent',related_name='children') 
	
	def __str__(self):

		return self.title

4.Run  ``python manage.py runserver`` Visit http://127.0.0.1:8000 to create users and its cards.

