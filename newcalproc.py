from yaml import load
import pytz, datetime, re, markdown, dateutil, unidecode, json

calStyFill = '''
.calendar { display: table; }
.calendar .week { display: table-row; }
.calendar .day { display: table-cell; height: 100%; }

.calendar .day.empty { background: white; opacity: 0.25; }

.calendar .day { 
    vertical-align: top; 
    background: rgba(255,255,255,0.25); 
    border: none; padding: 0.5ex 1ex;
    border-radius: 1ex;
}
.calendar { border-spacing: 1ex; }
.calendar { background: #84807c; border-radius:1.5ex; }

.calendar .event { padding: 0 1ex; margin: 0 -1ex; }
.calendar .event:last-child { padding-bottom: 0.5ex; margin-bottom: -0.5ex; border-bottom-left-radius: 1ex; border-bottom-right-radius: 1ex; }

.calendar time { display:none; }

.calendar .event { flex: 1 1 auto; }
.calendar .content { display: flex; flex-direction: column; height: calc(100% - 0.707em); }
.calendar .date { display: block; float: none; height: 1.414em; font-size: 70.7%; text-align: right; background-color: #ffddcc; margin: 0 -1.414ex; border-top-left-radius: 1.414ex; border-top-right-radius: 1.414ex; margin-top:-.707ex; padding: 0 1.414ex; }
'''

claStyNoflex = '''
.calendar { display: table; }
.calendar .week { display: table-row; }
.calendar .day { display: table-cell; height: 100%; }

.agenda { display: block; }
.agenda .week { display: block; }
.agenda .day { display: block; }

.calendar .day.empty { background: white; opacity: 0.125; }

.calendar .day { 
    vertical-align: top; 
    background: rgba(255,255,255,0.25); 
    border: none; padding: 0.5ex 1ex;
    border-radius: 1ex;
}
.calendar .date { 
    margin:-1.5ex -1.5ex 0 0; 
    font-size: 0.707em; 
    float: right; 
    padding: 0.5ex; 
    border-radius:1ex; 
    border-bottom-left-radius: 0;
    background: #ffddcc; 
}
.calendar { border-spacing: 1ex; }

.calendar { background: #84807c; border-radius:1.5ex; }

.calendar time { font-size: 50%; vertical-align: top; opacity:0.5; padding-right: 1ex; }

.calendar .event { padding: 0 1ex; margin: 0 -1ex; }
.calendar .event:first-child { padding-top: 0.5ex; margin-top: -0.5ex; border-top-left-radius: 1ex; border-top-right-radius: 1ex; }
.calendar .event:last-child { padding-bottom: 0.5ex; margin-bottom: -0.5ex; border-bottom-left-radius: 1ex; border-bottom-right-radius: 1ex; }
'''

ageSty = '''
.agenda { display: block; }
.agenda .week { display: block; }
.agenda .day { display: block; }

.agenda time { font-size: 70.7%; vertical-align: top; opacity:0.5; padding-right: 1ex; }

.agenda .day.empty { display: none; }

.agenda .day { display: flex; flex-direction: row; }
.agenda .day + .day { border-top: 0.125ex dotted #84807c; }

.agenda .week { border-top: 0.25ex solid #84807c; }

/*
.agenda .content { display: flex; flex-direction: row; width:100%; }
.agenda .event { flex: auto; padding: 0 0.5ex; }
*/

.agenda .content { display: flex; flex-direction: column; width:100%; }
.agenda .event { flex: auto; padding: 0 0.5ex; }


.agenda .date { font-size: 0.707em; font-family: monospace; margin-right: 1ex; white-space:pre; min-width:6em; }
.agenda .date.w0:before { content: "Sun "; }
.agenda .date.w1:before { content: "Mon "; }
.agenda .date.w2:before { content: "Tue "; }
.agenda .date.w3:before { content: "Wed "; }
.agenda .date.w4:before { content: "Thu "; }
.agenda .date.w5:before { content: "Fri "; }
.agenda .date.w6:before { content: "Sat "; }
.agenda .details { display: inline; }
.agenda .details:before { content: " "; }
'''

buttonScript = '''
var today = new Date().toISOString().substr(0,10);
document.querySelectorAll('.week').forEach(function(x){
    x.classList.add('past');
});
document.querySelectorAll('.day').forEach(function(x){
    if (x.getAttribute('date') < today) x.classList.add('past');
    else {
        if (x.getAttribute('date') == today) x.classList.add('today');
        else x.classList.add('future');
        x.parentElement.classList.remove('past');
    }
});
function saveCookie(key, value) {
    var d = new Date();
    d.setTime(d.getTime() + (365.24*24*60*60*1000)); // 1 year
    var expires = "expires="+ d.toUTCString();
    document.cookie = key + '=' + value + ";" + expires;
}
function viewmode(me) {
    if (me.value) me = me.value;
    document.getElementById('schedule').classList.remove('calendar');
    document.getElementById('schedule').classList.remove('agenda');
    document.getElementById('schedule').classList.add(me);
    saveCookie('viewmode', me);
    if (!document.getElementById('viewmode='+me).checked) {
        document.getElementById('viewmode='+me).checked = true;
    }
}
function show(me,val) {
    if (me.value) return show(me.value, me.checked);
    let css = document.getElementById('schedule-css');
    if (val) {
        for(let i=0; i<css.sheet.cssRules.length; i+=1) {
            if (css.sheet.cssRules[i].cssText == '.'+me+' { display: none; }') {
                css.sheet.deleteRule(i);
                break;
            }
        }
    } else {
        css.sheet.insertRule('.'+me+' { display: none; }');
    }
    saveCookie('view_'+me, val);
}
function showPast(visible) {
    if (typeof(visible) != 'boolean') visible = visible.checked;
    let css = document.getElementById('schedule-css');
    if (visible) {
        for(let i=0; i<css.sheet.cssRules.length; i+=1) {
            if (css.sheet.cssRules[i].cssText == '.calendar .week.past { display: none; }')
            { css.sheet.deleteRule(i); i-=1; }
            else if (css.sheet.cssRules[i].cssText == '.agenda .day.past { display: none; }')
            { css.sheet.deleteRule(i); i-=1; }
            else if (css.sheet.cssRules[i].cssText == '.agenda .week.past { display: none; }')
            { css.sheet.deleteRule(i); i-=1; }
        }
    } else {
        css.sheet.insertRule('.calendar .week.past { display: none; }');
        css.sheet.insertRule('.agenda .day.past { display: none; }');
        css.sheet.insertRule('.agenda .week.past { display: none; }');
    }
}
String(document.cookie).split('; ').forEach(function(x){
    x = x.split('=');
    if (x[0] == 'viewmode') viewmode(x[1]);
    else if (x[0].startsWith('view_')) {
        let input = document.querySelector('input[name="show"][value="'+x[0].substr(5)+'"]');
        if (input) {
            input.checked = x[1] == 'true';
            show(x[0].substr(5), input.checked);
        }
    }
});
'''

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

def prettyjson(d, newlineindent=2, maxinline=79):
    """The way I like to see JSON:
    commas begin lines
    short collections inline
    no extra spaces"""
    s = json.dumps(d, separators=(',',':'))
    indent = 0
    instr = False
    def skipshort(start, maxlen):
        """Given the starting index of a list or dict, returns either
        the same index, if it is too long,
        or the index of the last character of the list/dict"""
        nest = 0
        instr = False
        i = start
        comma = False
        while i < len(s) and ((not comma) or (i < start+maxlen)):
            if instr:
                if s[i] == '\\': i+=1
                elif s[i] == '"': instr = False
            else:
                if s[i] == '"': instr = True
                elif s[i] in '[{': nest += 1
                elif s[i] in ']}':
                    nest -= 1
                    if nest == 0: return i
                elif s[i] == ',': comma = True
            i += 1
        return start
    chunks = []
    i=0
    last=0
    indents = []
    while i < len(s):
        if instr:
            if s[i] == '\\': 
                i+=1
            elif s[i] == '"': instr = False
        elif s[i] == '"': instr = True
        else:
            if s[i] in '[{':
                end = skipshort(i, maxinline-(i-last)-indent)
                if end > i: i = end
                elif (i-last) < 8:
                    indents.append(indent)
                    indent += (i-last)
                else:
                    chunks.append(s[last:i])
                    indents.append(indent)
                    indent += newlineindent
                    chunks.append('\n'+' '*indent)
                    last = i
            elif s[i] in ']}':
                chunks.append(s[last:i])
                chunks.append('\n'+' '*indent + s[i])
                indent = indents.pop()
                last = i+1
            elif s[i] == ',':
                chunks.append(s[last:i])
                chunks.append('\n'+' '*indent)
                last = i
        i += 1
    if last < i: chunks.append(' '*indent + s[last:i])
    return ''.join(chunks)


def fixworking():
    """change to this script's directory as the working directory"""
    import os, os.path
    os.chdir(os.path.realpath(os.path.dirname(__file__)))

def slugify(s):
    """lower-case ascii with - instead of non-alphanum"""
    return re.sub(r'[^a-z0-9]+', '-', unidecode.unidecode(s).lower())

def dow(n):
    """string to int, with datetime's default 0=monday weekday numbering"""
    if type(n) is int: return n
    n = n.lower()
    if n.startswith('mo') or n == 'm': return 0
    if n.startswith('tu') or n == 't': return 1
    if n.startswith('we') or n == 'w': return 2
    if n.startswith('th') or n == 'h': return 3
    if n.startswith('fr') or n == 'f': return 4
    if n.startswith('sa') or n == 's': return 5
    if n.startswith('su') or n == 'u': return 6
    raise Exception("Unknown weekday: "+str(n))

def day(v):
    """convert to datetime.date (not datetime.datetime, as < is type-sensitive)"""
    if isinstance(v, datetime.datetime): return v.date()
    if isinstance(v, datetime.date): return v
    if isinstance(v, str): return day(dateutil.parser.parse(v))
    return datetime.datetime.fromtimestamp(v, default_tz).date()

def fixDate(yamldate, newtime=None, weekday=None, tz=None):
    """Add a time zone, possibly also changing time of day and/or day of week"""
    if tz is None: tz = default_tz
    if newtime is None:
        if isinstance(yamldate, datetime.datetime):
            newtime = yamldate.hour*60+yamldate.minute
        else:
            newtime = 12*60
    if type(weekday) is int: weekday = [weekday]
    if type(weekday) is list:
        ddows = [dow(_) - yamldate.weekday() for _ in weekday]
        ddows.sort()
        if ddows[0] < 7-ddows[-1]: yamldate += datetime.timedelta(ddows[0])
        else: yamldate += datetime.timedelta(ddows[-1]-7)
    return datetime.datetime(yamldate.year, yamldate.month, yamldate.day, newtime//60, newtime%60, 0, tzinfo=tz)

def shouldSkip(date, skips, pad=None):
    """Checks if a date is in a list of days to skip;
    also checks other days of the week if asked to do so"""
    if day(date) in skips: return True
    if pad is not None:
        for w in pad:
            if day(fixDate(date, weekday=w).date()) in skips:
                return True
    return False

def nextDOW(yamldate, weekdays, stayOK=False, skip=(), skippad=None):
    """Give a date and a list of days of the week, find the first day after this date that is one of those days of the week; optionally skipping some days"""
    ans = yamldate + datetime.timedelta(1-int(stayOK))
    ok = [dow(_) for _ in weekdays]
    while ans.weekday() not in ok or shouldSkip(ans, skip, skippad):
        ans += datetime.timedelta(1)
    return ans

def flatten(l):
    if type(l) in (str, int, bool): return [l]
    return [_2 for _1 in l for _2 in flatten(_1)]
    
def l2s(l, join=' <small>and</small> ', md=lambda x:x):
    if type(l) is str:
        return md(l)[3:-4].replace('<p>','').replace('</p>','')
    return join.join(l2s(_, join=join, md=md) for _ in flatten(l))


def plusMin(date, minutes):
    return date + datetime.timedelta(0,minutes*60)

def calendar(data, linkfile):
    """Given a yaml file, creates a calendar: a date-sorted sequence of entries
    Each entry contains some subset of
    
    - datetime data:
        - at least two of
            - open date
            - close date
            - duration
        - on a calendar, display as [close-duration, close] or [open, close] or [open, open+duration]
    - filter strings, including
        - type (lecture, lab, PA, Quiz, etc)
        - sections (a set of strings; None implies all)
    - title
    - hyperlink
    - textual details
    - submission info, including
        - filename globs
        - submission instructions
        - support files
        - tester to run
        - due date/time
    - grading rubric
    """
    
    name = data['meta']['name']
    month = data['Special Dates']['Courses begin'].month
    year = data['Special Dates']['Courses begin'].year
    finalurl = 'http://www.virginia.edu/registrar/exams.html#1{}{}'.format(year%100, month + (month == 1))
    calname = '{}.{}{}'.format(name, ('S' if month < 5 else 'Su' if  month < 8 else 'F'), year)
    lecexam = data['meta'].get('lecture exam',True)
    ans = []
    
    breaks = []
    exams = {}
    for k,v in data['Special Dates'].items():
        if 'recess' in k or 'break' in k or 'Reading' in k:
            if type(v) is dict: breaks.append((v['start'], v['end']))
            else: breaks.append((v, v))
        elif 'xam' in k or 'uiz' in k:
            exams[v] = k
    breaks, _breaks = [], breaks
    for s,e in _breaks:
        while s <= e:
            breaks.append(s)
            s += datetime.timedelta(1)
    breaks.append(day(fixDate(data['Special Dates']['Courses begin']) + datetime.timedelta(-1)))
    breaks.append(day(fixDate(data['Special Dates']['Courses end']) + datetime.timedelta(+1)))
    
    labDOW = flatten([[dow(_1) for _1 in _['days']] for _ in data['sections'].values() if _['type'] == 'lab'])
    
    # Lectures and labs 
    for sec, sdat in data['sections'].items():
        d = fixDate(data['Special Dates']['Courses begin'], newtime=sdat['start'])
        if sdat.get('type',sec) == 'lecture':
            skip=breaks[:]
            if lecexam: skip.extend(exams)
            d = nextDOW(d, sdat['days'], True, skip=skip)
            for top in data['lectures']:
                details = {
                    'start':d, 'end':plusMin(d, sdat['duration']),
                    'type':'lecture', 'section':sec,
                }
                if not top:
                    details['title'] = 'TBA'
                else:
                    if type(top) is str: top = [top]
                    details['title'] = l2s(top, md=markdown.markdown)
                    details['reading'] = l2s((data['reading'].get(_,()) for _ in top), md=markdown.markdown)
                    details['_reading'] = flatten([data['reading'][_] for _ in top if _ in data['reading']])
                    if not details['reading']: details.pop('reading')
                    if not details['_reading']: details.pop('_reading')
                
                if d.date() in linkfile:
                    links = []
                    for k,v in linkfile[d.date()].items():
                        if k in ['mp3','webm']: continue
                        if k != 'files':
                            links.append('['+k+']('+v+')')
                    links.extend('['+os.path.basename(_).replace('.html','')+']('+_+')' for _ in linkfile[d.date()].get('files',[]))
                    details['links'] = ' (lecture: '+l2s(links, md=markdown.markdown)+')'

                ans.append((d.timestamp(), details))
                d = nextDOW(d, sdat['days'], skip=skip)
            while day(d) <= day(data['Special Dates']['Courses end']):
                ans.append((d.timestamp(), {
                    'start':d, 'end':plusMin(d, sdat['duration']),
                    'type':'lecture', 'section':sec,
                    'title':'TBA',
                }))
                d = nextDOW(d, sdat['days'], skip=skip)
        elif sdat.get('type',sec) == 'lab':
            base = data['assignments'].get('.groups',{}).get('Lab',{}).get('base',None)
            skip=breaks[:]
            if not lecexam: skip.extend(exams)
            skip.extend(sdat.get('skip',()))
            d = nextDOW(d, sdat['days'], True, skip=skip, skippad=labDOW)
            num = 0
            for top in data['labs']:
                num += 1
                details = {
                    'start':d, 'end':plusMin(d, sdat['duration']),
                    'type':'lab', 'section':sec,
                }
                if not top:
                    details['title'] = 'TBA'
                else:
                    if type(top) is str: top={'title':top}
                    details['title'] = top.get('title', l2s(top.get('files', 'TBA')))
                    if 'link' in top: details['link'] = top['link']
                    elif 'title' in top and base is not None: 
                        details['link'] = base + 'lab{:02d}-'.format(num)+slugify(top['title'])+'.html'
                    
                ans.append((d.timestamp(), details))
                d = nextDOW(d, sdat['days'], skip=skip, skippad=labDOW)
            while day(d) <= day(data['Special Dates']['Courses end']):
                ans.append((d.timestamp(), {
                    'start':d, 'end':plusMin(d, sdat['duration']),
                    'type':'lab', 'section':sec,
                    'title':'TBA',
                }))
                d = nextDOW(d, sdat['days'], skip=skip)
    
    # assignments, quizzes, etc
    for task,tdat in data.get('assignments',{}).items():
        if task.startswith('.'): continue
        if tdat is None or 'due' not in tdat: continue
        print(task ,tdat)
        group = tdat.get('group', re.sub('^([A-Za-z]+).*',r'\1', task))
        for k,v in data['assignments'].get('.groups', {}).get(group, {}).items():
            if k not in tdat: tdat[k] = v
        
        end = fixDate(tdat['due'])
        start = plusMin(end, min(0,-tdat.get('duration', 0)))
        title = task
        if 'title' in tdat: title += ': ' + tdat['title']
        details = {
            'start':start, 'end':end,
            'type':group, 'title':title,
        }
        if 'link' in tdat: details['link'] = tdat['link']
        elif 'writeup' in tdat and 'base' in data['meta']: details['link'] = data['meta']['base'] + tdat['writeup']
        elif 'title' in tdat and 'base' in tdat:
            details['link'] = tdat['base'] + slugify(title)+'.html'
        ans.append((start.timestamp(), details))
    
    # Exams
    ans.append((fixDate(data['meta']['final']['start']).timestamp(),{
        'start':fixDate(data['meta']['final']['start']),
        'end':plusMin(fixDate(data['meta']['final']['start']), data['meta']['final']['duration']),
        'type':'Exam',
        'title':data['meta']['final'].get('title', exams.get(day(data['meta']['final']['start']), 'Final')),
        'link':data['meta']['final'].get('link', finalurl),
        'details':'in '+ data['meta']['final'].get('room', 'the usual classroom'),
    }))
    for e in exams:
        if day(e) >= day(data['Special Dates']['Courses end']):
            continue
        for sec,sdat in data['sections'].items():
            if (sdat['type'] == 'lecture') == data['meta'].get('lecture exam',True):
                start = fixDate(e, newtime=sdat['start'], weekday=sdat['days'])
                ans.append((start.timestamp(), {
                    'start':start, 'end':plusMin(start, sdat['duration']),
                    'type':'Exam', 'section':sec,
                    'title':exams[e]
                }))
    
    ans.sort(key=lambda a: (a[0], a[1].get('type','')))
    ans.insert(0, (0, calname, finalurl))
    return ans

def toIcal(events, sections=None, stamp=None):
    if stamp is None:
        now = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%S')
    else:
        now = stamp.astimezone(pytz.timezone('UTC')).strftime('%Y%m%dT%H%M%S')
    ans = ['''BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//University of Virginia//{0}//EN
CALSCALE:GREGORIAN
NAME:{0}'''.format(events[0][1])]
    def icescape(s):
        s = s.replace('"', '').replace(':', '')
        s = s.replace('\\', '\\\\')
        s = s.replace('\n', '\\n')
        s = s.replace(r',', r'\,')
        s = s.replace(r',', r'\;')
        return s
    for event in events[1:]:
        event = event[1]
        if 'section' in event and sections and event['section'] not in sections: continue
        details = []
        if 'details' in event: details.append(event.get('details'))
        if 'link' in event: details.append('see <' + event.get('link')+'>')
        if '_reading' in event: details.extend(event.get('_reading'))
        ans.append('''BEGIN:VEVENT
SUMMARY:{title}
DESCRIPTION:{notes}
DTSTART;TZID={tz};VALUE=DATE-TIME:{start}
DTEND;TZID={tz};VALUE=DATE-TIME:{end}
DTSTAMP;VALUE=DATE-TIME:{now}
UID:{uid}Z
END:VEVENT'''.format(
            title=event['type']+' -- ' + event.get('title', event.get('section', 'TBA')),
            start=event['start'].strftime('%Y%m%dT%H%M%S'),
            end=event['end'].strftime('%Y%m%dT%H%M%S'),
            tz=str(event['start'].tzinfo),
            uid=events[0][1]+'+'+event.get('title', event.get('type'))+'+'+event['start'].strftime('%Y%m%dT%H%M%S'),
            now=now,
            notes=icescape('\n'.join(details))
        ))
            
    ans.append('END:VCALENDAR\r\n')
    return '\r\n'.join(_.replace('\n','\r\n') for _ in ans)

def toHtml(events, sections=None):
    style = calStyFill + ageSty
    lastDay = day(events[1][-1]['start'])
    usedDOW = set(_[-1]['start'].weekday() for _ in events[1:])
    weekstart = 6 if 6 in usedDOW else min(usedDOW)
    haveContent = False
    while lastDay.weekday() != weekstart: lastDay -= datetime.timedelta(1)
    body = []
    body.extend(['<style id="schedule-css">', style, '</style>'])
    body.append('''<p>View as 
    <label><input type="radio" name="viewmode" onchange="viewmode(this)" value="calendar" id="viewmode=calendar"> calendar</label> or <label><input type="radio" name="viewmode" onchange="viewmode(this)" checked value="agenda" id="viewmode=agenda"> agenda</label>; <label><input type="checkbox" name="showpast" onclick="showPast(this)" checked> show past</label></p><p>View components''')
    body.append(', '.join([
       '<label><input type="checkbox" name="show" onchange="show(this)" value="{0}" checked> {0}</label>'.format(_) for _ in sorted(set(_1[1]['type'] for _1 in events[1:] if _1[1]['type'] not in ('lab','lecture')))+['reading'] + sorted(set(_1[1]['section'] for _1 in events[1:] if 'section' in _1[1]))
    ]))
    body.append('</p>')

    body.append('<table id="schedule" class="schedule agenda"><tr class="week"><td class="day" date="{2}"><span class="date w{1}">{0}</span>'.format(lastDay.strftime('%d %b').strip('0'), lastDay.strftime('%w'), lastDay.strftime('%Y-%m-%d')))
    for event in events[1:]:
        event = event[1]
        if 'section' in event and sections and event['section'] not in sections: continue
        s = day(event['start'])
        while s > lastDay:
            if haveContent:
                body.append('</div>')
                haveContent = False
            else:
                body[-1] = body[-1].replace('class="day"', 'class="day empty"')
            lastDay += datetime.timedelta(1)
            while lastDay.weekday() not in usedDOW:
                lastDay += datetime.timedelta(1)
            if lastDay.weekday() == weekstart:
                body.append('</td></tr><tr class="week">')
            else:
                body.append('</td>')
            body.append('<td class="day" date="{2}"><span class="date w{1}">{0}</span>'.format(lastDay.strftime('%d %b').strip('0'), lastDay.strftime('%w'), lastDay.strftime('%Y-%m-%d')))
        if not haveContent:
            haveContent = True
            body.append('<div class="content">')
        body.append(re.sub('<a href="">(.*?)</a>',r'\1','<div class="event {type} {section}"><time datetime="{dt}">{time}</time><a href="{link}">{title}</a><div class="details">{details}</div><div class="reading">{reading}{links}</div></div>'.format(
            link=event.get('link',''),
            title=event.get('title', 'TBA'),
            type=event.get('type',''),
            details=event.get('details',''),
            section=event.get('section',''),
            reading=event.get('reading',''),
            links=event.get('links',''),
            dt=event['start'].strftime('%Y-%m-%dT%H:%M:%S'),
            time=event['start'].strftime('%H:%M '),
        ).replace('<div class="details"></div>','').replace('<div class="reading"></div>','')))
    if haveContent:
        body.append('</div>')
        haveContent = False
    body.append('</td></tr>')
    body.append('</table>')
    body.extend(['<script>',buttonScript,'</script>'])
    return '\n'.join(body)

totaling_keys = ('portion', 'drop', 'include', 'exclude')
numgap = re.compile(r'([a-zA-Z])([0-9])')
codeclass = re.compile(r'[{][.][^}]+[}]')

def assignments_json(data):
    import collections
    groups = data['assignments'].get('.groups', {})
    ans = collections.OrderedDict()
    for k,v in data['assignments'].items():
        if k.startswith('.'): continue
        if v is None: ans[k] = {}
        else: ans[k] = {_k:_v for _k,_v in v.items() if not (_k.startswith('.') or _k in totaling_keys)}
        if 'group' not in ans[k]:
            for g in groups:
                if k.startswith(g):
                    ans[k]['group'] = g
        for ex,val in groups.get(ans[k].get('group',''), {}).items():
            if ex == '.tester-prefix' and 'files' in ans[k] and 'tester' not in ans[k]:
                if type(ans[k]['files']) is str:
                    ans[k]['tester'] = val + ans[k]['files']
                elif len(ans[k]['files']) == 1:
                    ans[k]['tester'] = val + ans[k]['files'][0]
            if ex.startswith('.') or ex in totaling_keys or ex in ans[k]: continue
            ans[k][ex] = val
        if 'title' not in ans[k] and ans[k].get('group',None) == 'PA' and type(ans[k].get('files',None)) is str:
            ans[k]['title'] = ans[k]['files']

    # fix date and datetime (to be a str) for JSON export
    for k,v in ans.items():
        for k2 in v:
            if isinstance(v[k2], datetime.datetime):
                try: # 3.6 and beyond
                    v[k2] = v[k2].isoformat(sep=' ', timespec='minutes')
                except: # not yet 3.6
                    v[k2] = v[k2].isoformat(sep=' ')[:4+1+2+1+2+1+2+1+2]
            elif isinstance(v[k2], datetime.date):
                if k2 == 'open':
                    v[k2] = v[k2].isoformat() + ' 00:00'
                else:
                    v[k2] = v[k2].isoformat() + ' 23:59'
    # sort by due date
    keys = [(v.get('due','~'+k),k) for k,v in ans.items()]
    keys.sort()
    for _,k in keys:
        ans.move_to_end(k)
    return ans

def coursegrade_json(data):
    groups = data['assignments'].get('.groups', {})
    weights, drops, inc, exc = {}, {}, {}, {}
    for k,v in groups.items():
        if 'portion' in v:
            weights[k] = v['portion']
        else:
            weights[k] = 0
        if type(weights[k]) is str:
            try:
                weights[k] = eval(weights[k].replace('%','/100'))
            except: pass
        if 'drop' in v:
            drops[k] = v['drop']
        if 'include' in v:
            inc[k] = v['include']
        if 'exclude' in v:
            exc[k] = v['exclude']
    for k,v in drops.items():
        if type(v) is str:
            v = eval(v.replace('%','/100'))
        if v < 1:
            cnt = 0
            for k,v in assignments_json(data).items():
                if v.get('group','') == k: cnt += 1
            v *= cnt
        drops[k] = int(round(v))
    return {'letters':[
        # {'A+':0.98},
        {'A' :0.93},
        {'A-':0.90},
        {'B+':0.86},
        {'B' :0.83},
        {'B-':0.80},
        {'C+':0.76},
        {'C' :0.73},
        {'C-':0.70},
        {'D+':0.66},
        {'D' :0.63},
        {'D-':0.60},
        {'F' :0.00},
    ],'weights':weights,'drops':drops,'includes':inc,'excludes':exc}

def yamlfile(f):
    global default_tz
    if type(f) is str:
        with open(f) as stream:
            data = load(stream, Loader=Loader)
    else:
        data = load(f, Loader=Loader)
    default_tz = pytz.timezone(data['meta'].get('timezone', 'America/New_York'))
    events = calendar(data)

    with open(f+'.ics', 'w') as ic:
        print(toIcal(events), file=ic)

    with open(f+'.html', 'w') as hm:
        print('''﻿<html><head><style>
        .Exam, .lab {{ background: #ddeeff; }}
        .lecture {{ background: white; }}
        .PA, .Quiz, .HW {{ background: #ffddcc; }}
        .PA:after, .Quiz:after {{ content: " due"; }}
        .agenda .CS2501-300:before {{ content: "Lec: "; }}
        .agenda .CS2501-301:before {{ content: "Lab: "; }}
        .agenda .CS2501-302:before {{ content: "Lab: "; }}
        .agenda .reading:before {{ content: "Reading: "; }}
        .agenda *:not(.date):before, small {{ opacity:0.707; font-size: 70.7%; }}
        .day.past {{ opacity: 0.5; }}
        /* .today {{ box-shadow: 0 0 1ex 1ex #ffddcc; }} */
        </style></head><body>{}</body></html>'''.format(toHtml(events)), file=hm)

def tomarkdown(f, links=None):
    global default_tz

    if type(f) is str:
        with open(f) as stream:
            data = load(stream, Loader=Loader)
    else:
        data = load(f, Loader=Loader)

    if type(links) is str:
        with open(links) as stream:
            links = load(stream, Loader=Loader)
    elif links is not None:
        links = load(links, Loader=Loader)

    default_tz = pytz.timezone(data['meta'].get('timezone', 'America/New_York'))
    print(links)
    events = calendar(data, links)

    with open('markdown/cal.ics', 'w') as ic:
        print(toIcal(events), file=ic)
    with open('markdown/schedule.html', 'w') as hm:
        print(toHtml(events), file=hm)
    with open('assignments.json', 'w') as f:
        f.write(prettyjson(assignments_json(data)))
    with open('coursegrade.json', 'w') as f:
        f.write(prettyjson(coursegrade_json(data), maxinline=16))






if __name__ == '__main__':
    import sys, os.path
    done = False
    
    for f in sys.argv[1:]:
        if os.path.exists(f):
            yamlfile(f)
        else:
            print('USAGE', sys.argv[0], 'calender.yaml [cal2.yaml ...]')
        done = True

    if not done:
        fixworking()
        tomarkdown('newcal.yaml', 'links.yaml')
