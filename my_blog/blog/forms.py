from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()  # Адрес эл. почты получателя
    comments = forms.CharField(required=False, widget=forms.Textarea)
    # У каждого типа поля есть заранее заданный виджет, который определяет
    # то, как поле прорисовывается в исходном коде HTML. Поле name является
    # экземпляром класса CharField. Поле этого типа прорисовывается как HTML-элемент <input type="text">.
    # Заранее заданный виджет можно переопределять
    # посредством атрибута widget. В поле comments используется виджет Textarea,
    # чтобы отображать его как HTML-элемент <textarea> вместо используемого
    # по умолчанию элемента <input>
