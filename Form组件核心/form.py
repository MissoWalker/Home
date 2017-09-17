import re
import copy

######################### 定制插件  #########################

class Input(object):
    def __init__(self, attrs=None):
        """
        :param attr: 生成的HTML属性，如：{'id': '123'}
        """
        self.attrs = attrs if attrs else {}

    def __str__(self):
        """
        override，使用对象返回的字符串
        :return:
        """
        t = "<input {0} />"
        attrs_list = []
        for k, v in self.attrs.items():
            temp = "{0}='{1}'".format(k, v)
            attrs_list.append(temp)
        tag = t.format(''.join(attrs_list))
        return tag

class TextInput(Input):
    def __init__(self, attrs=None):
        attr_dict = {'type':'text'}
        if attrs:
            attr_dict.update(attrs)
        super(TextInput,self).__init__(attr_dict)
    # def __str__(self):
    #     data_list = []
    #     for k, v in self.attrs.items():
    #         tmp = "{0} = '{1}'".format(k, v)
    #         data_list.append(tmp)
    #     tpl = "<input type='text' {0}>".format(" ".join(data_list))
    #     return tpl

######################### 定制字段（正则）  #########################
map()
reduce()
zip()
filter(function,[1,23,3])
class Field(object):

    def __str__(self):
        if self.value:
            self.widget.attrs['value'] = self.value

        return str(self.widget)

class CharField(Field):
    default_widget = TextInput
    regex = "\w+"
    def __init__(self,widget=None):
        self.value = None
        self.widget = widget if widget else self.default_widget()

    def valid_field(self,value):
        self.value = value
        if re.match(self.regex,value):
            return True
        else:
            return False

######################### 定制Form  #########################

class BaseForm(object):
    def __init__(self,data):
        self.fields = {}
        self.data = data
        for name,field in type(self).__dict__.items():
            if isinstance(field,Field):
                new_field = copy.deepcopy(field)
                setattr(self,name,new_field)
                self.fields[name] = new_field
    def is_valid(self):
        flag = True
        for name, field in self.fields.items():
            user_input_val = self.data.get(name)
            result = field.valid_field(user_input_val)
            if not result:
                flag = False
        return flag




class LoginForm(BaseForm):
    uers = CharField()

 #form = LoginForm(request)
form = LoginForm({"user":'zms','email':'zms@aaa.com'})


