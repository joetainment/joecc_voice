

class Conf:
    class Test:
            tmp=0

    phrases4on = [
    'voice typing start',
    'voice taking start',
    'voiced typing start',
    'voiced taking start',
    ]
    
    phrases4off = [
    'voice typing stop',
    'voice taking stop',
    'voiced typing stop',
    'voiced taking stop',
    ]
        
    phrases4turnoff = [
    'voice typing turn off',
    'voice taking turn off',
    'voice taping turn off',
    
    'voiced typing turn off',
    'voiced taking turn off',
    'voiced taping turn off',
    
    'voice typing turn of',
    ]

    """
    ## this can p0
    l4=[
    
    "alpha", "bravo", "charlie",
    
    ]
    """
    
    
    ## mapStringsToNatoMany
    s2w = {
    'tells the':'alpha',
    'of the':'alpha',
    'off the':'alpha',
    'off of':'alpha',
    'off a':'alpha',
    'all from':'alpha',
    'health of':'alpha',
    
    
    'alpha phi alpha':'alpha alpha',
    'will self':'alpha alpha',
    'all files':'alpha alpha',
    'profile from':'alpha alpha',
    
    'brown will':'bravo',
    
    'have co':'echo',
    'pepco':'echo',
    
    '12th':'golf',
    'goal for':'golf',
    'goal of':'golf',
    'go off':'golf',
    
    'and in':'india',
    'can be a':'india',
    'candy a':'india',
    'in via a':'india',
    
    
    ' in november':' november',  ## Intentional space
    
    'cost are':'oscar',
    
    
    'pop of':'papa',
    'pop off':'papa',
    
    'tank of':'tango',
    
    'echospace':'echo space',
    
    'pack only in the':'echo lima',
    'back only my':'echo lima',
    'goal from hoster':'golf oscar',
    'call for oscar':'golf oscar',
    'golf cluster':'golf oscar',
    
    'hotel of some':'hotel alpha',
    'hotel from':'hotel alpha',
    'hotel also':'hotel alpha',
    'hotel room to':'hotel alpha',
    'hotel room from':'hotel alpha',
    'hotel well from':'hotel alpha',
    'hotel will flow':'hotel alpha',
    
    'and entangle':'india tango',
    
    
    'bema ,  the':'lima papa',
    'bema , the':'lima papa',
    'fema ,  the':'lima papa',
    'fema , the':'lima papa',
    'lima ,  the':'lima papa',
    'lima,':'lima papa',
    'lima, the':'lima papa',
    
    
    
    'brown locale from':'bravo alpha',
    
    'michael foale':'mike alpha',
    'november 12':'november golf',
    
    'c airspace':'sierra space',
    'c areospace':'sierra space',
    'c aroespace':'sierra space',
    
    'we scraped':'whiskey',
    'in kiosk are':'yankee oscar',
    
    'back slash'  :  'backslash',
    # 'travels', 'space', 'charlie', 'brown', 'loafers'
    }
    
    ## mapStringsToNatoSingle
    map = {
    'alfa':'alpha',
    'alfie':'alpha',
    'alfred':'alpha',
    'loafers':'alpha', 
    'also':'alpha',   
    'alfalfa':'alphaAlpha',
    'calpha':'alpha',
    'often':'alpha',
    'call for':'alpha',
    'balpha':'alpha',
    'al from':'alpha',
    
    'travels':'bravo',
    'travel':'bravo',
    'gravel':'bravo',
    'bracco':'bravo',
    
    
    
    'journey':'charlie',
    'charles':'charlie',
    
    'ago':'echo',
    'tobacco':'echo',
    'vacco':'echo',
    'echoed':'echo',
    'nikko':'echo',
    'until':'echo',
    'deco':'echo',
    'echospace':'echo space',
    
    'gulf':'golf',
    'golfer':'golf',
    'cove':'golf',
    'calls':'golf',
    'called':'golf',
    
    'indian':'india',
    
    'julia':'juliet',
    
    'bema':'lima',
    'fema':'lima',
    
    'might':'mike',
    'mic':'mike',
    
    'defender':'november',
    "november's":'november',
    
    'foster':'oscar',
    'oskar':'oscar',
    'poster':'oscar',
    
    'popup':'papa',
    'pop up':'papa',
    'pop of':'papa',
    'poppel':'papa',
    
    'only a little for':'romeo',
    
    
    
    
    'uniformly much':'uniform lima',
    
    '12':'golf',
    'twelve':'golf',
    #12:'golf',
    
    'tangles':'tango',
    
    
    'gandhi':'yankee',
    'kinky':'yankee',
    'healthy':'yankee',
    
    'base':'space',
    
    'inter':'enter',
    
    'shifts':'shift',
    
    'spaceship':'space shift',
    'space-shift':'space shift',
    'ciara':'sierra',
    
    'tape':'type',
    'take':'type',
    'tight':'type',
    'text':'type',
    'types':'type',
    'typed':'type',
    'tie':'type',
    'te':'type',
    'title':'type',
    'tate':'type',
    
    'up':'',
    
    'with ski':'whiskey',
    
    #')' :     ' ) ',
    #'(' :     ' ( ',
    
    
    #'also':'alpha',
    # e d     'equitable', 'to'    'if', 'the', 'bill', 'to'  
    
    # shift    schiff
    
    # c e d      'charlie', 'acquittal', 'to'
    
    # i     indio
    
    # l l     'in', 'the', 'name', 'a'
    
    # m          'mine', 'to',
    
    }
    
    
    
    symbs = (
        
        'alpha',
        'bravo',
        'charlie',
        'delta',
        'echo',
        'foxtrot',
        'golf',
        'hotel',
        'india',
        'juliet',
        'kilo',
        'lima',
        'mike',
        'november',
        'oscar',
        'papa',
        'quebec',
        'romeo',
        'sierra',
        'tango',
        'uniform',
        'victor',
        'whiskey',
        'x-ray',
        'yankee',
        'zulu',
        'zero',
        'one',
        'two',
        'three',
        'four',
        'five',
        'six',
        'seven',
        'eight',
        'nine',
        
        
        'period',
        'dot',
        'point',
        'comma',
        'colon',
        'semi-colon',
        'question mark',
        'slash',
        
        'backspace',
        
        'space',
    )
    
    symsense = [( '', 0.9 ) ] + [ (symb,0.001) for symb in symbs ]
    print( symsense )


    ## mapNatoToKb
    w2kb = {
        'voice typing start':'',
        'voice typing stop':'',
        
        'alpha':'a',
        'alphaAlpha':'aa',
        
        'bravo':'b',
        'charlie':'c',
        'delta':'d',
        'echo':'e',
        'foxtrot':'f',
        'golf':'g',
        'hotel':'h',
        'india':'i',
        'juliet':'j',
        'kilo':'k',
        'lima':'l',
        'mike':'m',
        'november':'n',
        'oscar':'o',
        'papa':'p',
        'quebec':'q',
        'romeo':'r',
        'sierra':'s',
        'tango':'t',
        'uniform':'u',
        'victor':'v',
        'whiskey':'w',
        'xray':'x',
        'yankee':'y',
        'zulu':'z',
        
        'zero':'0',
        'one':'1',
        'two':'2',
        'three':'3',
        'four':'4',
        'five':'5',
        'six':'6',
        'seven':'7',
        'eight':'8',
        'nine':'9',
        
        '0':'0',
        '1':'1',
        '2':'2',
        '3':'3',
        '4':'4',
        '5':'5',
        '6':'6',
        '7':'7',
        '8':'8',
        '9':'9',
        
        #'zero':'0',
        #'zero':'0',
        
        #'tab':'tab',
        #'backspace':'backspace',
        
        'space':' ',
        'enter':'\n',
        
        ','  :  ',',
        'comma'  :  ',',
        
        
        ';'  :  ';'  ,
        'semicolon'  :  ';'  ,
        'semi-colon'  :  ';'  ,
        
        ':'  :  ':'  ,
        'colon'  :  ':'  ,
        
        
        
        '.'  :  '.'  ,
        'peroid'  :  '.'  ,
        'dot'  :  '.'  ,
        'point'  :  '.'  ,
        
        '?':'?',
        '!':'!',
        
        '-'  :  '-'  ,
        'dash'  :  '-'  ,
        'hyphen'  :  '-'  ,
        'minus'  :  '-'  ,
        
        '_' : '_',
        'underscore' : '_',
        
        
        
        
        'quote'  :  '"',
        
        'apostrophe'  :  "'"  ,
        "'"  :  "'"  ,
        
        '='  :  '='  ,
        'equals'  :  '='  ,
        
        '+'  :  '+'  ,
        'plus'  :  '+'  ,
        
        
        '['  :  '['  ,
        ']'  :  ']'  ,
        '('  :  '('  ,
        ')'  :  ')'  ,
        '{'  :  '{'  ,
        '}'  :  '}'  ,
        
        '<' : '<',
        'less' : '<',
        '>' : '>',
        'greater' : '>',
        
        'slash'  :  '/',
        'backslash'  :  '\\',
    }