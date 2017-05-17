# my-life-for-Aiur

基于[对RBAC的理解](http://blog.thrimbda.com/2017/05/06/RBAC%E5%AE%9E%E8%B7%B5%E7%B3%BB%E7%BB%9F%E8%AE%BE%E8%AE%A1/)，也由于作业要求，我将编写一个简单的Demo对作为RBAC的实践。

我无意将Demo做的无比庞大，我的目标在于说明问题，所以依然”麻雀虽小，五脏俱全。“

那么这个Demo的目标是什么呢，他都可以做些什么呢？

部署：
```bash
#  dependencies
pip install -r requirements.txt

#  run server
gunicorn -b 0.0.0.0:$PORT src.API:app
```

## 分析与设计

为了有趣并充分反映问题，我将在自己的Demo中模拟一个大幅简化的、每个单位都奇迹般地拥有了主观能动性的星际争霸 (StarCraft) 战局中一位星灵玩家所面对的场景。

一个好的Demo需要一个好的名字，因此这个Demo的名字叫做：**为了艾尔！**（艾尔是星灵的母星，每个狂热者在被传送到战场时都会说这样一句慷慨激昂的话：”为艾尔而战！“）

在**为了艾尔**中，你要带领着己方队伍生产出足够的狂热者战士，消灭毁灭者埃蒙，拯救整个宇宙，如果你的狂热者不够，你将会失败，群星低语，万物湮灭。

这一切都体现在一个由python的flask框架所编写的RESTful的服务中。

> 其实真实的场景中除玩家外每个主体都可以被创造出来，因此都可以被视为资源，而为了体现RBAC，我给他们添加了如下约束：
>
> - 本Demo所提供的几个主体唯一并且始终存在，就如同他们是独一无二的一样，因此也除去任何主体可以被递归地创造出来的可能（例如：探机可以生产星灵枢纽，而星灵枢纽可以生产探机）
> - 事实上传送门是需要水晶的能量支持才能运作的，但是在这里没有体现出来，我将其解释为我们的传送门受到了位于同步轨道上亚顿之矛这艘星灵的传奇母舰的能量支持，从而只把水晶塔看作提供人口上限的资源。

这个战局中拥有以下对象：

### 主体(Subject)

- 玩家 （你）thrimbda
- 探机 （基本的工作单位，可以采集生产资源，也可以建造建筑）probe
- 传送门 （生产狂热者，一种作战单位）gatewat

#### 角色(Role)

- 执政官（最高统帅，调配一切资源）archon
- 晶体矿采集者 （只有探机可以承担此任）crystal_collector
- 供狂热者传送的枢纽 （支持星灵战士折跃的信标）portal
- 水晶建造者 （有了水晶，我们才可以有足够的人口上限用来传送狂热者）pylon_transporter

### 资源 (Resource)

- 未采集的水晶矿 （用于建造水晶，以及传送狂热者，初始值未知）
- 采集的水晶矿 （用于建造水晶，以及传送狂热者，初始值0）
- 产能 （提供传送的能量，也就是我们口中的人口，初始值0）
- 狂热者 （作战单位，你用来拯救宇宙的战士们，初始值0）

### 权限 (Permission)

> 由于针对资源的每一个操作都是一个权限，因此这里我们不单独把操作列出，而直接给出权限及其描述

- 采集晶矿（每次最多采集1000单位）
- 观察未采集的晶矿（观察总量）
- 状态报告 （报告当前你所拥有的资源数量）
- 侦察埃蒙的实力（计算需要的狂热者数量）
- 建造水晶塔（每个水晶塔提供10的产能单位，以及100晶矿）
- 生产狂热者（每个狂热者消耗2的产能单位，以及100晶矿）
- 攻击埃蒙（不胜利，毋宁死！）

### SA

> 主体-角色以及角色-权限的多对多关系，使用python的多元祖数据结构表示，在实现中亦是如此，因此本应用中不使用数据库。

```python
subject_role = (('thrimbda', 'archon'),
                ('probe', 'crystal_collector'),
                ('probe', 'pylon_transporter'),
                ('gateway', 'portal'))
```

### PA

```python
role_permission = (('archon', 'get_status'),
                   ('archon', 'for_aiur'),
                   ('archon', 'scout'),
                   ('crystal_collector', 'get_crystal'),
                   ('crystal_collector', 'crystal_status'),
                   ('pylon_transporter', 'get_status'),
                   ('pylon_transporter', 'transport_pylon'),
                   ('portal', 'transport_zealot'),
                   ('portal', 'get_status'))
```



## 实现

[线上部署](https://my-life-for-aiur.herokuapp.com/)（速度慢）

### 综述

总的来说我使用了python的flask框架编写了一个RESTful风格的服务，整个应用不涉及前端部分，因此也不存在绕过前端等安全问题了。

首先这个Demo的一个特点在于没有使用数据库，RBAC并没有强制使用数据库，且在RBAC中使用数据库是符合直觉的意见很自然的事情，但在**为了艾尔**中我们不使用数据库，而是使用文件的形式体现RBAC的`主体-角色-权限`关系。数据库本身就是在文件系统的基础上发展而来的，这里采用文件是因为系统足够简单，为了说明问题而进一步降低系统的复杂度。具体的文件形式见上述 SA, PA 关系说明。

### 有关RESTful

这里简单地提以下RESTful(**Re**presentational **S**tate **T**ransfer)

顾名思义，（资源的）表现层状态转化

在一个Web服务中，提供的服务即为系统的资源，以URI的形式体现，而服务的形式为对资源的操作（状态转化），以HTTP动词的形式体现。这其中的几个概念可以很好地跟RBAC中资源、操作对应起来，因此我要做的就是将RBAC中的权限管理应用在REST中对资源的操作上。

### RBAC中各个对象

可以看到在这两个配置文件中，除了SA和PA之外，我们可以隐含地求得S、R、P：

```python
# 根据上述元组 subject_role 求得S、R列表
subjects = list(set([item[0] for item in subject_role]))
roles = list(set([item[1] for item in subject_role]))
```

而SE可以很好地和web应用中的session对应起来，作为一个主体在一次登陆中的一个临时对象：

```python
# 主体用来登陆亚顿之矛战术管理系统的API，这里session作为flask的一个全局对象，其实现细节不再赘述。
class SpearOfAdun(Resource):
    
    def post(self):
        args = self.putparser.parse_args()
        if args['subject'] is not None:
            abortInvalideSubject(args['subject'])
        if args['role'] is not None:
            abortInvalideRole(args['role'])
        checkRole(args['subject'], args['role'], subject_role)
        session['subject'] = args['subject']
        session['role'] = args['role']
        return {'message': 'login as %s using %s' % (session['subject'], session['role'])}, 201
```

由于主体-角色的建模最终是为了将权限隔离开后分配，使得系统中的资源能够被妥善使用与保护。

在**为了艾尔**中，我将权限作为web API的内部属性，例如:

```python
# 用来传送狂热者的API
class Zealot(Resource):

    def put(self):
        permission = 'transport_zealot' # 权限
        abortIfSubjectUnauthenticated(session) # 登陆验证
        checkPermission(session['role'], permission, role_permission) # 鉴定主体在此角色下是否可以请求此权限
        args = self.putparser.parse_args()
        amount = nexus.transport(args['amount'])
        return {'message': 'transport %d zealot warriors, En Taro Tassadar!' % amount}, 200
```

而在上述用来举例的两个API中每个类都作为系统中的一个资源而存在，而提供的HTTP方法则是对资源的操作。

**至此，RBAC中的几种对象都到齐啦。**

### 业务逻辑

由于**为了艾尔**是一个真实可玩的在线即时战略类游戏API，因此有必要讲讲它的业务逻辑：

玩家的目标是：**收集资源，建造基地，然后创造一支令你的敌人闻风丧胆的部队打败黑暗者埃蒙。**

打败埃蒙的唯一条件就是要拥有足够数量的狂热者（zealot），而这个数量为系统随机生成的一个20到100之间的整数，同时系统会根据这个数据生成刚好够你打败埃蒙的未采集晶矿。

**为什么是刚好够？**

由于传送狂热者需要足够数量的水晶能量以及晶矿，提供能量的水晶塔也需要消耗晶矿来生产。因此假如你建造了太多的水晶塔，那么虽然水晶能量够了，但你会**因为没有足够的晶矿来传送狂热者而输掉这场决定整个宇宙命运的战役**。

而整套逻辑由一个生命周期跨越整场战役的对象提供，为了防止问题，我加入了线程锁来确保每个操作都是原子的。

```python
# 由于它是整个游戏的核心，我将它称之为枢纽-Nexus
import random
from threading import Lock


class Nexus(object):
    _lock = Lock()
    crestalInControl = None
    crestalRemain = None
    populationCap = None
    zealot = None
    status = {}
    _amond = None

    def __init__(self):
        # 初始化对象
        self._amond = random.randint(20, 100)
        self.crestalRemain = self._amond * 100 + (self._amond // 5 + 1) * 100
        self.crestalInControl = 0
        self.populationCap = 0
        self.zealot = 0

    def collect(self, amount=1000):
        # 采集水晶矿
        with self._lock:
            amount = min(amount, self.crestalRemain)
            self.crestalRemain -= amount
            self.crestalInControl += amount
            return amount

    def transport(self, amount=5):
        # 传送狂热者
        with self._lock:
            capacity = self.populationCap / 2
            available = self.crestalInControl / 100
            amount = min(amount, capacity, available)
            self.zealot += amount
            self.crestalInControl -= amount * 100
            self.populationCap -= amount * 2
            return amount

    def build(self, amount=1):
        # 建造水晶塔
        with self._lock:
            available = self.crestalInControl / 100
            amount = min(amount, available)
            self.populationCap += amount * 10
            self.crestalInControl -= amount * 100
            return amount

    def forAiur(self):
        # 为艾尔而战！
        with self._lock:
            if self.zealot >= self._amond:
                return True
            else:
                return False

    def getStatus(self, role):
        # 获取状态
        if role == 'archon':
            return {
                'crestalInControl': self.crestalInControl,
                'crestalRemain': self.crestalRemain,
                'populationCap': self.populationCap,
                'zealot': self.zealot
            }
        elif role == 'pylon_transporter':
            return {
                'crestalInControl': self.crestalInControl,
                'populationCap': self.populationCap
            }
        elif role == 'portal':
            return {
                'crestalInControl': self.crestalInControl,
                'populationCap': self.populationCap,
                'zealot': self.zealot
            }
        else:
            return {}


nexus = Nexus() # 实例化对象
```

## 结语

其实星际争霸二这个游戏在每场战局中都是一个典型的DAC模型：玩家主宰一切，而游戏中所有的操作都可以看作是将水晶矿和高能瓦斯（在我这里被简化掉了）这两种基础资源进行状态转化，成为玩家所需要的资源（生产单位，作战单位）并去消耗敌方的资源从而赢得战局。这说明RESTful服务的思想非常普适。

在**为了艾尔**这个小游戏中，我将几种角色固化，构造了一个RBAC模型。

在这次实践中，理解了RBAC在一个系统中的应用，并且进一步学习了flask这个超赞的框架，更加深入地理解了RESTful思想，收获良多。