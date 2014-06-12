from flask.ext.wtf import Form
from wtforms import fields,validators,SubmitField
from flask.ext.codemirror.fields import CodeMirrorField

class UserForm(Form):
    basecamp_number = fields.StringField('Account Number',validators=[validators.Required()])
    basecamp_username = fields.StringField('Username',validators=[validators.Required()])
    basecamp_password = fields.PasswordField('Password',validators=[validators.Required()])

class CommentForm(Form):
    source_code = CodeMirrorField(language="python",config={'lineNumbers':'true','matchingbracket':'true','lines':'true','cursor':'true'})
    submit = SubmitField('submit')

