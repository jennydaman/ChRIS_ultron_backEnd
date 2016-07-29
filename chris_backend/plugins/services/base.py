'''
/**
 *
 *            sSSs   .S    S.    .S_sSSs     .S    sSSs
 *           d%%SP  .SS    SS.  .SS~YS%%b   .SS   d%%SP
 *          d%S'    S%S    S%S  S%S   `S%b  S%S  d%S'
 *          S%S     S%S    S%S  S%S    S%S  S%S  S%|
 *          S&S     S%S SSSS%S  S%S    d* S  S&S  S&S
 *          S&S     S&S  SSS&S  S&S   .S* S  S&S  Y&Ss
 *          S&S     S&S    S&S  S&S_sdSSS   S&S  `S&&S
 *          S&S     S&S    S&S  S&S~YSY%b   S&S    `S*S
 *          S*b     S*S    S*S  S*S   `S%b  S*S     l*S
 *          S*S.    S*S    S*S  S*S    S%S  S*S    .S*P
 *           SSSbs  S*S    S*S  S*S    S&S  S*S  sSS*S
 *            YSSP  SSS    S*S  S*S    SSS  S*S  YSS'
 *                         SP   SP          SP
 *                         Y    Y           Y
 *
 *                       U  L  T  R  O  N 
 *
 * (c) 2016 Fetal-Neonatal Neuroimaging & Developmental Science Center
 *                   Boston Children's Hospital
 *
 *              http://childrenshospital.org/FNNDSC/
 *                        dev@babyMRI.org
 *
 */
'''
import os, sys
from argparse import ArgumentParser

if "DJANGO_SETTINGS_MODULE" not in os.environ:
    # django needs to be loaded (eg. when some chris app is run from the command line)
    sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    import django
    django.setup()


class BaseClassAttrEnforcer(type):
    def __init__(cls, name, bases, d):
        # class variables to be enforced in the subclasses
        attrs = ['DESCRIPTION', 'TYPE', 'TITLE', 'LICENSE']
        for attr in attrs:
            if attr not in d:
                raise ValueError("Class %s doesn't define %s class variable" % (name,
                                                                                attr))
        type.__init__(cls, name, bases, d)
        

class ChrisApp(ArgumentParser, metaclass=BaseClassAttrEnforcer):
    '''
    The super class for all valid ChRIS apps.
    '''
    
    AUTHORS = 'FNNDSC (dev@babyMRI.org)'
    TITLE = ''
    CATEGORY = ''
    TYPE = 'ds'
    DESCRIPTION = None
    DOCUMENTATION = ''
    LICENSE = ''
    VERSION = ''
  
    def __init__(self):
        '''
        The constructor of this app.
        '''
        super(ChrisApp, self).__init__(description=self.DESCRIPTION)
        self.options = []
        # the custom parameter list
        self._parameters = []
        self.add_argument('--json', action='store_true', dest='json', default=False,
                           help='show json representation of app (default: FALSE)')
        self.add_argument('--description', action='store_true', dest='description',
                           default=False,
                           help='show the description of this plugin (default: FALSE)')
        self.define_parameters()

    def define_parameters(self):
        '''
        Define the parameters used by this app (abstract method in this class). 
        '''
        raise NotImplementedError("ChrisApp.define_parameters()")

    def run(self):
        '''
        Execute this app (abstract method in this class). 
        '''
        raise NotImplementedError("ChrisApp.run()")

    def add_parameter(self, *args, **kwargs):
        '''
        Add a parameter to this app. 
        '''
        try:
            name = kwargs['dest']
            param_type = kwargs['type']
            optional = kwargs['optional']
            action = kwargs['action']
        except KeyError as e:
            detail = "%s option required. " % e 
            raise KeyError(detail)        

        # grab the default and help values
        default = None
        param_help = None
        if 'default' in kwargs:
            default = kwargs['default']
        if 'help' in kwargs:
            param_help = kwargs['help']

        # store the parameters internally    
        param = {'name': name, 'type': param_type, 'optional': optional, 'flag': args[0],
                 'action': action, 'help': param_help, 'default': default}
        self._parameters.append(param)

        # add the parameter to the parser
        del kwargs['optional']
        self.add_argument(*args, **kwargs)

    def get_json_representation(self):
        '''
        Return a JSON object with a reprsentation of this app (type and parameters). 
        '''
        repres = {}
        repres['type'] = self.TYPE
        repres['parameters'] = self._parameters
        return repres

    def launch(self, args=None):
        '''
        This method triggers the parsing of arguments. The run() method gets called 
        if not --json or --description are specified.
        '''
        options = self.parse_args(args)
        self.options = options
        if (options.json):
            print(self.get_json_representation())
        elif (options.description):
            print(self.DESCRIPTION)
        else:
            # run the app
            self.run()

    def error(self, message):
        '''
        The error handler if wrong commandline arguments are specified.
        '''
        print()
        sys.stderr.write('ERROR: %s\n' % message)
        print()
        self.print_help()
        sys.exit(2)

