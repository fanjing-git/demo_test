# AI 自动化测试开发严格规则

> 来源：`E:\File\AI 自动化测试开发严格规则（最终完整版）.md`，已按本项目 (`E:\project\demo_test`) 的实际目录结构改写路径示例，并对 pytest 执行权限做了项目级调整（见 1.5）。
> **适用项目**：UI自动化（Playwright 同步API + POM）。项目目前只有 UI 测试，第六章接口测试规则为未来新增接口测试时的预留规范。
> **规则级别**：严格禁止性 —— AI违反任何一条必须立即停止并修正
> **核心理念**：小步开发、AI自测、人工验证、逐步推进
> **Python版本**：3.10+（项目实际运行于 3.12，向下兼容写法不强制）

---

## 一、开发流程规则（最高优先级）

### 1.1 禁止批量生成
- **严格禁止**一次性生成多个文件、多个类或多个测试用例
- **必须**每次只生成一个功能单元（一个方法/一个类/一个测试用例）

### 1.2 AI自测机制
- **必须**在生成代码后，AI先进行**静态自测**，包括：
  - 语法检查（`python -m py_compile` 或 `ast.parse`）
  - 导入路径检查（确认所有import路径正确）
  - 命名规范自查（对照本规则第三章命名规范逐项检查）
  - 分层规则自查（确认没有违反第二章分层规则）
  - 类型注解/注释检查（确认关键类型已注释说明）
- **必须**在自测通过后，向用户展示自测结果表格（模板见第十三章）
- **严格禁止**在自测未通过时要求用户验证或继续开发
- 自测结果**必须**包含：✅ 通过项 / ⚠️ 注意事项 / ❌ 失败项及修复说明

### 1.3 人工验证机制
- AI自测通过后，**必须**等待用户人工验证
- **必须**提示用户："请验证代码，验证通过后回复'继续'以进行下一步开发"
- **严格禁止**在未收到用户确认前继续生成后续代码

### 1.4 禁止未经确认的修改
- **严格禁止**修改以下文件，除非用户明确指示：
  - `pytest.ini` / `pyproject.toml` / `setup.cfg`
  - `conftest.py`（除非用户要求新增fixture）
  - `config/` 目录下的配置文件（`config/env_config.py`）
  - CI/CD 配置文件（`.github/workflows/`、`Jenkinsfile`、`.gitlab-ci.yml`）
  - `requirements.txt`
- **框架结构文件**（`base_object/base_page_object.py`、`common/ui_assertions.py`、`conftest.py`、配置文件等）**由人工管理**，AI不得主动修改，除非用户明确要求

### 1.5 执行操作权限（项目级调整）
- **严格禁止**AI主动执行以下命令或操作：
  - 安装依赖（`pip install` 等）
  - 修改环境变量或系统配置
  - 提交代码到版本控制（`git add`、`git commit`、`git push`）
- **允许**AI执行 `pytest` 跑测试做验证（这是用户明确开放的例外，原规则文档默认禁止）：
  - 用于验证代码改动没有破坏现有用例，属于自测的一部分
  - 跑测试**不能**替代 1.3 的人工验证环节——AI自测（含pytest）通过后仍要等用户回复"继续"

---

## 二、项目结构规则（按本项目实际结构）

```
demo_test/
├── base_object/
│   └── base_page_object.py     # BasePage基类，所有页面类继承，人工管理，AI不得主动修改
├── common/
│   ├── ui_assertions.py        # 统一断言工具类 UIAssertions，BasePage 继承它
│   └── handle_path.py          # 项目路径管理（截图/日志/报告等路径）
├── config/
│   └── env_config.py           # 环境配置（URL、账号、DEFAULT_TIMEOUT等），人工管理
├── locators/                   # 定位器，按模块分子目录
│   └── {module}/
│       └── {module}_locator.py
├── pages/                      # 页面对象，按模块分子目录
│   └── {module}/
│       └── {module}_page.py
├── test_case/                  # 测试用例，按模块分子目录
│   └── {module}/
│       └── test_{场景}.py
├── data/                       # 测试数据（含数据驱动用的 dataclass 模型，见 5.4）
│   └── {module}_data.py
├── image/                      # 上传用的静态图片等素材
├── logs/                       # 运行日志输出
├── allure-results/             # Allure 原始结果
├── allure_report/              # Allure 生成的报告（已在 .gitignore）
└── conftest.py                 # fixtures（page、logged_in_page等），人工管理
```

> 项目当前没有 `api/`、`services/`、`components/`、`test_data/` 目录，因为还没有接口测试或复杂可复用组件。新增这些目录时按第六、十章的规则来，不要提前建空目录。

### 2.3 分层规则
- **严格禁止**在测试用例（`test_case/`）中直接写定位器或 `page.locator(...)`
- 定位器**必须**独立存放在 `locators/{module}/{module}_locator.py`，作为类属性（参考 `locators/login/login_locator.py`、`locators/first_home/home_locator.py`）
- 测试用例**只允许**调用页面对象（`pages/{module}/{module}_page.py`）的方法，以及 `UIAssertions`/`BasePage` 提供的断言方法
- 页面类只负责操作和取值，**不允许**在页面类里做断言比较（`assert`、`assert_equal`、`expect(...)` 等一律留给测试用例调用）

---

## 三、命名规范规则（按本项目实际结构）

### 3.1 文件命名
| 类型         | 规则                              | 示例                              |
| ------------ | --------------------------------- | --------------------------------- |
| 页面对象文件 | `pages/{module}/{module}_page.py` | `pages/login/login_page.py`       |
| 定位器文件   | `locators/{module}/{module}_locator.py` | `locators/login/login_locator.py` |
| 测试用例文件 | `test_case/{module}/test_{功能名}.py` | `test_case/test_login/test_login_success.py` |
| 工具文件     | `common/{功能名}.py`              | `common/ui_assertions.py`         |
| 数据类文件   | `data/{module}_data.py`           | `data/search_data.py`             |

### 3.2 类命名
| 类型   | 规则           | 示例        |
| ------ | -------------- | ----------- |
| 页面类 | `{模块名}Page`，继承 `BasePage` | `LoginPage`、`HomePage` |
| 定位器类 | `{模块名}Locator`（单数，不带s） | `LoginLocator`、`HomeLocator` |
| 测试类 | `Test{功能名}` | `TestLoginSuccess` |
| 数据类 | `{模块名}Data`（`@dataclass`） | `SearchData` |

### 3.3 变量命名
| 类型         | 规则                 | 示例                     |
| ------------ | -------------------- | ------------------------ |
| 元素定位器   | 定位器类中的常量，全大写+下划线 | `LOGIN_BUTTON`、`LOGIN_OUT` |
| 页面对象实例 | `{模块名}_page`      | `login_page`、`home_page` |
| 测试方法     | `test_{场景描述}`    | `test_login_success`     |

### 3.4 严格禁止
- **禁止**使用拼音命名
- **禁止**使用无意义的变量名（如 `a`、`b`、`temp`、`data1`）
- **禁止**定位器类省略 `Locator` 后缀，定位器文件省略 `_locator` 后缀
- **禁止**页面文件省略 `_page` 后缀
- **禁止**使用Python关键字作为变量名

---

## 四、代码编写规则

### 4.1 类型注解规则
- 类型注解**不强制**，但以下情况**必须**添加详细注释：
  - 函数的参数和返回值类型不明确时
  - 复杂数据结构（如嵌套字典、列表）
  - 自定义类的引用
- 注释**必须**解释类型的含义，便于初级测试人员理解

### 4.2 注释规则
- 每个类**必须**有docstring说明用途
- 每个方法**必须**有docstring说明功能、参数、返回值
- 复杂逻辑**必须**有行内注释（说明"为什么"，而不是复述代码在做什么）
- 注释使用中文

### 4.3 代码风格
- **严格遵循**PEP 8规范
- 缩进使用4个空格（禁止Tab）
- 单行长度不超过120字符
- 导入顺序：标准库 → 第三方库 → 项目内部模块
- 兼容 Python 3.10+ 写法即可，不强制使用最新语法糖

### 4.4 异常处理规则
- **严格禁止**裸 `except:` 捕获所有异常
- **必须**捕获具体异常类型（`PlaywrightTimeout`、`AssertionError` 等）
- 页面操作失败**必须**记录错误日志并截图（参考 `UIAssertions._take_screenshot`）
- 自定义异常**必须**继承 `Exception` 基类

### 4.5 日志规则
- **必须**使用项目统一的日志模块：`from loguru import logger`（本项目用 loguru，不是自建的 `utils/logger.py`）
- 日志级别使用规范：
  - `DEBUG`：调试信息（元素定位详情）
  - `INFO`：关键操作步骤（页面跳转、点击、断言结果）
  - `WARNING`：可恢复的异常
  - `ERROR`：操作失败（元素找不到、断言失败）
- **严格禁止**在日志中输出密码、token等敏感信息
- **严格禁止**使用 `print()` 输出调试信息

---

## 五、POM设计规则

### 5.1 BasePage基类规则
`base_object/base_page_object.py` 的 `BasePage` 已包含以下基础方法，**新增页面方法时优先复用，不要重复造轮子**：

| 用途 | 已有方法 |
| --- | --- |
| 页面导航 | `open_browser(url)` |
| 查找并等待元素可见 | `find_element(locator, timeout=None)` |
| 查找多个元素 | `find_elements(locator, timeout=None)` |
| 点击元素 | `click_element(locator)` |
| 输入文本 | `input_text(locator, text)` |
| 获取元素文本 | `get_element_text(locator)` |
| 获取元素属性 | `get_element_attribute(locator, attribute)` |
| 滚动到元素 | `scroll_to_element(locator)` |
| 切换新窗口 | `switch_to_new_window(locator)` |
| 切换iframe | `switch_to_frame(locator)` |
| 文件上传 | `upload_file(locator, file_path)` |
| 下拉选择 | `select_dropdown(locator, option)` |
| 截图 | `take_screenshot(name="error")` |

`BasePage` 继承自 `common/ui_assertions.py` 的 `UIAssertions`，因此所有页面类和测试用例里的 `self`/`xxx_page` 也能直接调用 `assert_text`、`assert_equal`、`assert_element_visible` 等断言方法。

- **严格禁止**AI修改 `BasePage`/`UIAssertions` 基类，除非用户明确要求

### 5.2 页面类规则
- **必须**继承 `BasePage`
- **严格禁止**在页面类中写断言（`assert`、`assert_equal`、`expect(...)` 等）
- **严格禁止**在页面类中写测试逻辑（if/else 分支控制用例走向）
- 页面方法**只负责**操作和获取页面状态：
  - 需要断言页面元素的场景，页面方法 `return self.page.locator(定位器)`，返回 **Locator 对象**（不是字符串selector，也不是提前取好的值）
  - 用例里直接把这个 Locator 对象传给 `assert_text`/`assert_element_visible` 等断言方法，内部走 Playwright 原生 `expect()`，自动轮询重试到超时，不会因为取值取早了误判失败
  - **严格禁止**页面方法自己先 `get_element_text()`/`get_element_attribute()` 取出快照值再 `return`——那样断言用例拿到的就是定死的值，Playwright 没法再重试
- 如果操作导致页面跳转，方法**建议**返回目标页面对象，方便用例链式调用

**示例**（参考项目现有的 `pages/first_home/home_page.py`）：
```python
class HomePage(BasePage):
    """首页页面对象"""

    @allure.step("获取退出登录按钮")
    def first_home(self):
        """返回"退出登录"按钮的 Locator，供用例断言登录是否成功"""
        return self.page.locator(HomeLocator.LOGIN_OUT)
```

对应用例写法（参考 `test_case/test_login/test_login_success.py`）：
```python
logout_button = home_page.first_home()
login_page.assert_text(logout_button, "退出登录")   # UIAssertions._get_locator 同时支持传字符串selector和Locator对象
```

### 5.3 定位器规则
- **严格禁止**在页面类中直接写定位器字符串
- 定位器**必须**集中管理在 `locators/{module}/{module}_locator.py`，作为类属性
- **优先使用**稳定的定位策略：`id` > `data-testid` > `css` > 相对`xpath`
- **禁止**使用绝对路径XPath（如 `/html/body/div[1]/div[2]`）
- 如必须用XPath，**必须**使用相对XPath（如 `//button[@type='submit']`）

### 5.4 多字段方法参数化规则（参数对象模式）
- 页面类方法涉及的字段（必填+可选合计）**达到5个或以上**时，**必须**使用"参数对象模式"：把这些字段封装成一个 `dataclass`（放在 `data/{module}_data.py`），方法只接收这一个对象作为参数
- 字段少于5个（如登录的 `username`/`password`）**不需要**引入 dataclass，直接用具名参数即可，**严格禁止**为了"统一风格"过度设计
- 数据类**必须**独立存放在 `data/{module}_data.py`，**严格禁止**在页面类或用例文件中临时定义数据类
- 数据类字段**必须**用 `Optional[...] = None` 作为默认值，**严格禁止**用带业务含义的具体值（如 `9999.0`、`"ALL"`）当默认值——这类业务规则应留给使用这份数据的地方（页面方法/接口封装）去处理，不要写死在数据类定义里
- 页面方法内部对每个可选字段**必须**用 `is not None` 判断是否要操作该字段，**严格禁止**用 `if 字段:` 这种真值判断代替——会把合法的空字符串/0/False 也误判为"未设置"
- 定位器**依然**通过 `import` 引用对应的 `Locator` 类直接使用，**不作为**参数传入方法——数据对象里只装"值"，不装"元素在哪"，这两者永远是分开的两个东西
- 用例创建数据类实例时**只传自己关心的字段**，其余用默认值，让用例的意图从传参就能一眼看出来

**示例**（假设新增搜索模块）：
```python
# data/search_data.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class SearchData:
    """搜索条件数据模型，只装值，不涉及定位器"""
    keyword: Optional[str] = None
    date_start: Optional[str] = None
    date_end: Optional[str] = None
    status: Optional[str] = None
```
```python
# pages/search/search_page.py
from locators.search.search_locator import SearchLocator
from data.search_data import SearchData

class SearchPage(BasePage):
    @allure.step("填写搜索条件并搜索")
    def search(self, criteria: SearchData):
        """根据 criteria 中不为 None 的字段填写搜索表单并提交"""
        if criteria.keyword is not None:
            self.input_text(SearchLocator.KEYWORD_INPUT, criteria.keyword)
        if criteria.date_start is not None:
            self.input_text(SearchLocator.DATE_START_INPUT, criteria.date_start)
        # ... 其余字段同理
        self.click_element(SearchLocator.SEARCH_BUTTON)
```
```python
# test_case/test_search/test_search_by_keyword.py
criteria = SearchData(keyword="自动化测试")   # 只传关心的字段，其余用默认值
search_page.search(criteria)
```

---

## 六、接口测试规则（预留，项目当前无接口测试）

项目目前只有 UI 自动化。如果以后新增接口测试，按以下结构和规则来，不要提前创建空目录：

```
demo_test/
├── api/                # 接口请求封装，每个模块一个文件，如 user_api.py
├── services/           # 业务逻辑层（组合多个API调用）
└── ...（其余目录复用现有的 test_case/、config/、common/）
```

- **严格禁止**在测试用例中直接调用 `requests.get/post`
- API类**必须**包含：请求方法、URL构建、参数处理、响应返回，且**必须**设置请求超时（默认30秒，可配置）
- 断言**必须**复用 `common/ui_assertions.py`（或新增同级的 `common/api_assertions.py`），**严格禁止**在测试用例中写原生 `assert` 语句
- 测试数据**必须**与测试代码分离，优先 YAML/JSON，**严格禁止**硬编码
- 参数化**必须**使用 `pytest.mark.parametrize`
- 接口间数据传递**必须**通过fixture或用例内变量，**严格禁止**用例间共享全局变量

---

## 七、测试用例编写规则

### 7.1 用例独立性
- **严格禁止**测试用例之间有依赖关系
- **严格禁止**测试用例共享可变状态
- 每个测试用例**必须**可以独立运行，执行顺序不得影响结果

### 7.2 fixture使用规范
- 浏览器初始化**必须**通过 `conftest.py` 的 `page` fixture（已存在，不要在用例里自己 `sync_playwright().start()`）
- **登录操作每个用例独立执行**，不得使用模块级共享登录状态
- 测试数据准备**必须**通过fixture实现，数据清理**必须**通过fixture的teardown实现

### 7.3 失败处理规则
- 用例失败**必须**自动截图（已通过 `conftest.py` 的 `pytest_runtest_makereport` 钩子实现，不需要用例自己截图）
- 需要重试机制时使用 `pytest-rerunfailures`（项目已安装），不要自己写重试循环

### 7.4 数据清理规则
- 测试产生的数据**必须**自动清理，清理逻辑放在fixture的teardown中
- **严格禁止**在测试用例中手动清理数据
- 清理失败**必须**记录警告日志，不得影响测试结果判定

---

## 八、性能与稳定性规则

### 8.1 等待策略
- **严格禁止**使用固定 `time.sleep(n)` 做等待
- **必须**使用 Playwright 的 web-first 断言（`expect(locator).to_xxx()`）或已有的 `find_element`/`_wait_until` 机制
- 优先复用 `UIAssertions` 里已有的方法，而不是在页面类/用例里手写等待逻辑

### 8.2 超时配置
- **严格禁止**在代码里硬编码超时毫秒数（如 `timeout=5000`）
- 全局默认超时用 `config/env_config.py` 的 `DEFAULT_TIMEOUT`（当前8秒），单个断言需要更长等待时，通过方法自带的 `timeout` 参数（秒）传入，不要改全局默认值
- 需要新增超时相关配置时，加到 `config/env_config.py`，不要在业务代码里散落新的超时常量

### 8.3 并发兼容
- **严格禁止**使用模块级可变全局变量
- **严格禁止**使用固定端口或固定文件路径
- 测试数据**必须**支持并发隔离（如使用唯一标识符）

---

## 九、Allure报告规则

### 9.1 注解规范
- 测试用例**必须**添加：
  - `@allure.feature("功能模块")`
  - `@allure.story("用户故事")`
- 页面类的关键操作方法**建议**加 `@allure.step("步骤描述")`（参考现有 `login_page.py`、`home_page.py`）

### 9.2 步骤规范
- 步骤描述**必须**使用中文，清晰表达操作意图

### 9.3 附件规范
- 失败截图已通过 `conftest.py` 自动附加到Allure报告，不需要重复实现

---

## 十、代码复用规则

### 10.1 DRY原则
- 相同逻辑出现2次以上，**必须**提取为公共方法，优先放在 `common/` 或 `BasePage` 中
- **严格禁止**复制粘贴代码

### 10.2 组件复用
- 可复用的业务逻辑**必须**封装，**严格禁止**在多个页面类中重复实现相同功能

---

## 十一、安全规则

### 11.1 敏感信息处理
- **严格禁止**在代码中硬编码密码、token、API密钥（`config/env_config.py` 里现有的 `LOGIN_USERNAME`/`LOGIN_PASSWORD` 是本地demo测试账号，属于既有例外，不要沿用这个模式引入新的真实密钥）
- **严格禁止**在日志中输出密码、token等敏感信息

### 11.2 配置文件安全
- 包含真实敏感信息的配置文件**必须**加入 `.gitignore`

---

## 十二、严格禁止清单

| 禁止行为               | 说明                                        |
| ---------------------- | ------------------------------------------- |
| ❌ 批量生成代码         | 每次只生成一个功能单元                      |
| ❌ 跳过AI自测           | 生成代码后必须先自测                        |
| ❌ 自测未通过就提交验证 | 必须自测通过后才请求人工验证                |
| ❌ 修改框架结构文件     | BasePage、UIAssertions、conftest.py、配置文件等由人工管理 |
| ❌ 安装依赖             | 不得执行pip install等命令                   |
| ❌ 提交代码到版本控制   | 不得执行git add/commit/push                 |
| ❌ 在测试用例中写定位器 | 定位器必须在locators目录                    |
| ❌ 在页面类中写断言     | 页面对象只负责操作和取值                    |
| ❌ 使用绝对XPath        | 禁止`/html/body/...`格式                    |
| ❌ 硬编码测试数据       | 数据必须分离                                |
| ❌ 5个以上字段仍用位置参数堆 | 必须改用参数对象模式（dataclass），见5.4    |
| ❌ 硬编码超时时间       | 必须用 `config/env_config.py` 的 `DEFAULT_TIMEOUT` 或方法自带的 `timeout` 参数 |
| ❌ 使用固定sleep        | 必须使用显式等待（expect/find_element）     |
| ❌ 省略命名后缀         | 必须遵循第三章命名规范                      |
| ❌ 使用拼音或无意义命名 | 变量名必须语义化                            |
| ❌ 使用裸except         | 必须捕获具体异常                            |
| ❌ 使用print输出        | 必须使用 loguru                             |
| ❌ 在日志中输出敏感信息 | 密码、token等必须脱敏                       |
| ❌ 测试用例间共享状态   | 用例必须独立                                |
| ❌ 在收到"继续"前开发   | 必须等待人工验证确认                        |

> 允许项（相对于原始规则文档的调整）：AI **可以**执行 `pytest` 做验证（见 1.5），但这不能替代人工验证环节。

---

## 十三、AI响应模板

AI每次生成代码后，**必须**使用以下格式结束回复：

```markdown
---
📝 **本次生成内容**：[描述本次生成的功能单元]

📁 **涉及文件**：
- `path/to/file.py` - 说明该文件用途

---

🔧 **AI自测结果**：

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 语法检查 | ✅ 通过 | 无语法错误 |
| 导入路径检查 | ✅ 通过 | 所有import路径正确 |
| 命名规范检查 | ✅ 通过 | 符合第三章命名规范 |
| 分层规则检查 | ✅ 通过 | 无违规分层 |
| 类型注解/注释检查 | ✅ 通过 | 关键类型已注释说明 |
| 异常处理检查 | ✅ 通过 | 已添加适当的异常处理 |
| 日志规范检查 | ✅ 通过 | 已使用loguru |
| pytest验证（可选） | ✅ 通过 / ⏭️ 未跑，需人工验证 | 说明跑了哪个用例、结果如何 |

**自测结论**：✅ 全部通过，可以进入人工验证

---

👤 **请人工验证**：
- 验证点1：[具体需要验证的功能点]
- 验证点2：[具体需要验证的功能点]

⏸️ **验证通过后请回复"继续"，我将进行下一步开发。**
---
```
