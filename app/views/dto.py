# -*- coding: utf-8 -*-
from config import params

InputsSchema = {params['input.id']:{'required':True,'type':'string'},
                params['input.url']:{'required':True,'type':'string'},
                params['input.path']:{'required':True,'type':'string'},
                params['input.origin']:{'required':True,'type':'string'},
                params['input.user']:{'required':True,'type':'string'}}
