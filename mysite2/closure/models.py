
from django.db import models

# Create your models here.

"""
create table nodes (
node int auto_increment primary key,
label varchar(20) not null
);
"""

class Node(models.Model):
	label = models.CharField(max_length=20)
	

"""
create table closure (
ancestor int not null,
descendant int not null,
primary key (ancestor, descendant),
foreign key (ancestor) references nodes(node),
foreign key (descendant) references nodes(node)
);
"""

class Cl_tab(models.Model):
	ancestor = models.ForeignKey(Node)
	descendant = models.IntegerField(default=0)	
	level = models.IntegerField()