from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from polls.models import Question

from django.db import connection


def getTable(cursor):
    s = '<table style="width:100%">'
    for row in cursor.fetchall():
       #s = s + '<tr><td>' + str(row[0]) + '</td><td>' + row[1] + '</td></tr>'

       e = ''
       for i in range(len(row)):
           e += '<td>' + str( row[i] ) + '</td>'
       s = s + '<tr>' + e + '</tr>'

    s += "</table>"
    return s



def index(request):
    
    #return HttpResponse("Hello, world. You're at the polls index.")
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #output = ', '.join([p.question_text for p in latest_question_list])
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM nodes ")
    row = getTable(cursor)
    
    print( row )
    
    output = row
    return HttpResponse(output)

'''
SELECT group_concat(n1.label, '-'), n2.label, count(*) FROM closure
 join nodes n1 on (ancestor = n1.node)
  join nodes n2 on (descendant = n2.node)
  group by descendant
'''

def getTree(cursor, cnt, lab, id):
    s = '<table style="width:100%">'
    for row in cursor.fetchall():
       #s = s + '<tr><td>' + str(row[0]) + '</td><td>' + row[1] + '</td></tr>'

       e = ''
       for i in range(row[cnt] - 1):
           e += '<td> </td>'

       e += '<td> - \ </td>'

       e += '<td><a href="/closure/'+ str(row[id]) +'/tree/">' + row[lab] +'</a></td>'
       s = s + '<tr>' + e + '</tr>'

    s += "</table>"
    return s

def getAncestors(id):
    cursor = connection.cursor()
    cursor.execute("select p.ancestor , (select count(*) from closure gp where p.ancestor = gp.descendant) gen "
                    +" from closure p where  p.descendant = "+ str(id)
                    #+" order by gen desc "
                   )

    txt = ''
    for row in cursor.fetchall():
        txt += '<a  href="/closure/'+ str(row[0]) +'/tree/">'+ str(row[0]) +'</a> - '

    return '<p>'+ txt +'</p>'



def detail_tree(request, closure_id):

    ancestors = getAncestors(closure_id)

    cursor = connection.cursor()
    cursor.execute("SELECT group_concat(n.label, '-'), n.label, count(*), n.node "
                    +" FROM closure d"
                    +"   join closure a on (d.descendant = a.descendant) "
                    +"   join nodes n on (a.ancestor = n.node) "
                    +" where d.ancestor = "+ str(closure_id)
                    +" group by d.descendant"
                    #+" having ancestor = "+ str(question_id)
                    )
    tree = getTree(cursor, 2, 1, 3)
    resp = ancestors + '<p>'+ tree +'</p>'


    return HttpResponse(resp)


def detail_tree0(request, question_id):
    cursor = connection.cursor()
    cursor.execute("SELECT group_concat(n1.label, '-'), n2.label, count(*) FROM closure "
                    +" join nodes n1 on (ancestor = n1.node) "
                    +" join nodes n2 on (descendant = n2.node) "
                    +" where n1.node = "+ str(question_id)
                    +" group by descendant"
                    #+" having ancestor = "+ str(question_id)
                    )
    row = getTree(cursor, 2, 1)
    return HttpResponse(row)


def detail(request, question_id):
    cursor = connection.cursor()
    cursor.execute("SELECT n1.label, n2.label FROM closure "
                    +" join nodes n1 on (ancestor = n1.node) "
                    +" join nodes n2 on (descendant = n2.node) "
                    )
    row = getTable(cursor)
    return HttpResponse(row)

def detail_ancestor(request, question_id):
    cursor = connection.cursor()
    cursor.execute("SELECT n1.label, n2.label FROM closure "
                    +" join nodes n1 on (ancestor = n1.node) "
                    +" join nodes n2 on (descendant = n2.node) "
                    +" where descendant = "+ str(question_id)
                    )
    row = getTable(cursor)
    return HttpResponse(row)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
