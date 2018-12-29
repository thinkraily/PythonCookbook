1.2 从任意长度的可迭代对象中分解元素
1.2.1 问题	Problem
需要从某个可迭代对象中分解出N个元素,但是这个可迭代对象的长度可能超过N,这个会导致出现"分解的值过多(too many values to unpack)"的异常.
You need to unpack N elements from an iterable,but the iterable may be longer than N elements,causing a "too many values to unpack"exception.
1.2.2 解决方案	Solution
Python 的"*表达式"可以用来解决这个问题.例如,假设开设了一门课程,并决定在期末的作业成绩中去掉第一个和最后一个,支队中间剩下的成绩做平均分统计.如果只有4个成绩,也许可以简单地将4个都分解出来,但是如果有24个呢?*表达式使这一切都变得简单:
Python "star expressions" can be used to address this problem.For example,suppose you run a course and decide at the end of the semester that you're going to drop the firest and last homework grades,and only average the rest of them.If there are only four assignements,maybe you simply unpack all four,but what if there are 24?A star expression makes it easy:

def drop_firest_last(grades):
	first,*middle,last= grades
	return avg(middle)

另一个用例是假设有一些用户记录,记录由姓名和电子邮件地址组成,后面跟着任意数量的电话号码.则可以像这样分解记录:
As another use case,suppose you have user records that consist of a name and email address,followed by an arbitrary number of phone numbers.You could unpack the records like this:

>>> record = ('Steven','steven@example.com','773-555-1212','847-555-1212')
>>> name,email,*phone_numbers = user_record
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'user_record' is not defined
>>> name,email,*phone_numbers = record
>>> name
'Steven'
>>> email
'steven@example.com'
>>> phone_numbers
['773-555-1212', '847-555-1212']
>>>

不管需要分解出多少个电话号码(甚至没有电话号码),变量phone_numbers都一直是列表,而这是毫无意义的.如此一来,对于任何用到了变量phone_numbers的代码都不必对它可能不是一个列表的情况负责,或者额外做任何形式的类型检查.
#It's worth nothing that the phone_numbers variable will always be alist,regardless of how many phone numbers are unpacked(including none).Thus,any code that uses phone_numbers won't have to account for the possibility that it might not be a list or perform any kind of additional type checking.

有*修饰的变量也可以位于列表的第一个位置。例如，比方说用一系列的值来代表公司过去8个季度的销售额。如果想对最近一个季度的销售额通前7个季度的平均值做比较，可以这么做：
#The starred variable can alse be the firest one in the list.For example,say you have a sequence of values representing your company's sales figures for the last eight quarters.If you want to see how the most recent quarter stacks up to the average of the first seven,you cold do something like this:

*trailing_qtrs,current_qtr = sales_record
trailing_avg = sum(trailing_qtrs) / len(trailing_qtrs)
return avg_comparison(trailing_avg,current_qtr)

从Python解释器的角度来看，这个操作是这样的：
#Here's a view of the operation from the Python interpreter:

>>> *trailing,current=[10,8,7,1,9,5,10,3]
>>> trailing
[10, 8, 7, 1, 9, 5, 10]
>>> current
3
>>>

1.2.3 讨论	Discussion
对于分解未知或任意长度的可迭代对象，这种扩展的分解操作可谓是量身定做的工具。通常，这类可迭代对象中会有一些已知的组件或模式（例如，元素1之后的所有内容都是电话号码），利用*表达式分解可迭代对象是的开发者能够轻松利用这些模式，而不必再可迭代对象中做复杂花哨的操作才能得到相关的元素。
*式的语法在迭代一个变长的远足序列时尤其有用。例如，假设有一个代表及的元组序列：
Extended iterable unpacking is tailor-mode for unpacking iterables of unknown or arbitrary length.Oftentimes,these iterables have some known component or pattern in their construction(e.g."everything after element 1 is a phone number"),and star unpacking lets the developer leverage those patterns easily instead of performing acrobatics to get at the relevant elements in the iterable.
It is worth nothing that the star syntax can be especially useful when iterating over a sequence of tuples of varying length.For example,Perhaps a sequence of tagged tuples;

records =[
	('foo',1,2),
	('bar','hello'),
	('foo',3,4),
]

def do_foo(x,y):
	print('foo',x,y)

def do_bar(s):
	print('bar',s)

for tag,*args in records:
	if tag =='foo'
		do_foo(*args)
	elif tag =='bar':
		do_bar(*args)

当和某些特定的字符串处理操作相结合，比如拆分（splitting）操作时，这种*式的语法所支持的分解操作也非常游泳。例如：
Star unpacking can also useful when combined with certain kinds of string processing operations,such as splitting.For example:
>>> line = 'nobody:*:-2:-2:Unprivileged User:/var/empty:/user/bin/fales'
>>> uname,*fields,homedir,sh= line.split(':')
>>> uname
'nobody'
>>> homedir
'/var/empty'
>>> sh
'/user/bin/fales'
>>>

有时候可能向分解出某些值然后丢弃他们。在分解的时候，不能只是制定一个单独的*，但是可以使用几个常用来表示待丢弃值的变量名，比如_或者ign(ignored).例如：
Sometimes you might want to unpack values and throw them away.You can't just specify a bare * when unpacking,but you could use a common throwaway variable name,such as _ or ign(ignord).For example:

>>> record =('ACME',50,123.45,(12,18,2012))
>>> name,*_,(*_,year)= record
>>> name
'ACME'
>>> year
2012

*分解操作和各种函数式语言中的列表处理功能有着一定的相似性。例如，如果有一个列表，可以像下面这样轻松将其分解为头部和尾部：
There is a certain similarity between star unpacking and list-processing features of various functional languages.For example,if you have a list,you can easily split it into head and tail components like this:
>>> items =[1,10,7,4,5,9]
>>> head,*tail = items
>>> head
1
>>> tail
[10, 7, 4, 5, 9]
>>>

在编写执行这类拆分功能的函数时，人们可以假设这是为了实现某种精巧的递归算法。例如
One could imagine writing functions that perform such splitting in order to carry out some kind of clever recursive algorithm.For example:

>>> def sum(items):
...     head,*tail=items
...     return head + sum(tail) if tail else head
...
>>> sum(items)
36
>>>

但是请注意，递归真的不是Python的强项，这是因为其内在的递归限制所致。因此，最后一个例子在实践中没太大的意义，只不过是一点算术上的好奇罢了。
However,be aware that recursion really isn't a strong Python feature due to the inherent recursion limit.Thus,this last example might be nothing more than an academic curiosity in practice.
