from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect #, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Ma_Part, Mn_Name
from .models import Choice
import pandas as pd
import math

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
#q = Question.objects.filter( pub_date__lte=timezone.now() ).order_by('-pub_date')
          
        q = Question.objects.filter( pub_date__lte=timezone.now(),
            choice__isnull=False
            ).distinct()
        q = q.order_by('-pub_date')
        
        
        #q = Question.objects.raw("select * from polls_question")
        
        """for c in q:
            if len(c.choice_set.all()) == 0:
                #print(q, "XXXXXXX")
                q = q.exclude(id=c.id)
        """
        
            
        return q[:5]
    
        
        
class DetailView(generic.DetailView):
    model = Question
    #template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
        

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
         

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
        
#class Ma_PartView(generic.ListView):
    #


from django.http import HttpResponse


def listParts():
    parts = Ma_Part.objects.all() #.order_by('ma_desc')

    output = ''
    i = 0
    for p in parts:
        print i, p
        print str(p.ma_id),'|', p.ma_desc,'|', p.mn_id.mn_name,'|', p.mn_nr

        try:
            output += '<p>{0}: {1}  - {2}: {3}</p>'.format(str(p.ma_id), unicode(p.ma_desc), p.mn_id.mn_name, p.mn_nr)
        except:
            print "*************"
            pass
        print i, p.ma_id, p.ma_desc
        i += 1
    return output


def indexHello(request):
    output = listParts()
    return HttpResponse( output )


def listDf(df):
    output = ''
    for i in df.index:
        if math.isnan( df.iloc[i]['mamut nr'] ):
            print 'Next', i
            continue
            
            
        output += '<p>%d\t%s\t%s</p>' % (i, df.iloc[i][6], df.iloc[i]['levr pro nr'],) 
        mn, c = Mn_Name.objects.get_or_create(mn_name=df.iloc[i][6]) 
        mn.save()  
        
        output += '<p>%d\t%d\t%s</p>' % (i, df.iloc[i]['mamut nr'], df.iloc[i]['beskrivelse'],)
        p = Ma_Part.objects.get_or_create(ma_id=df.iloc[i]['mamut nr'], ma_desc=df.iloc[i]['beskrivelse'], mn_id=mn, mn_nr=df.iloc[i]['levr pro nr'], mn_desc='')
        print p
        
        try: 
            p.save()
        except:
            pass
        print i
        
        
        
        #output += '<p>%d\t%d\t%s</p>' % (i, df.iloc[i][6], df.iloc[i]['levr pro nr'],)
        #print p.mn_id
        #output += '<p>{0}: {1}  - {2}: {3}</p>'.format(str(p.ma_id), p.ma_desc, p.mn_id.mn_name, p.mn_nr)
    return output
    
    
def indexHello2(request):
    import pandas as pd
    df = pd.read_csv("parts-ax200", sep='\t')
    
    output = listDf(df) 
    #$listParts()
    return HttpResponse( output )

