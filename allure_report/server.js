
        function _base64ToArrayBuffer(base64) {
            var binary_string = window.atob(base64);
            var len = binary_string.length;
            var bytes = new Uint8Array(len);
            for (var i = 0; i < len; i++) {
                bytes[i] = binary_string.charCodeAt(i);
            }
            return bytes.buffer;
        }

        function _arrayBufferToBase64( buffer ) {
          var binary = '';
          var bytes = new Uint8Array( buffer );
          var len = bytes.byteLength;
          for (var i = 0; i < len; i++) {
             binary += String.fromCharCode( bytes[ i ] );
          }
          return window.btoa( binary );
        }

        document.addEventListener("DOMContentLoaded", function() {
            var old_prefilter = jQuery.htmlPrefilter;

            jQuery.htmlPrefilter = function(v) {
            
                var regs = [
                    /<a[^>]*href="(?<url>[^"]*)"[^>]*>/gi,
                    /<img[^>]*src="(?<url>[^"]*)"\/?>/gi,
                    /<source[^>]*src="(?<url>[^"]*)"/gi
                ];
                
                var replaces = {};

                for (i in regs)
                {
                    reg = regs[i];

                    var m = true;
                    var n = 0;
                    while (m && n < 100)
                    {
                        n += 1;
                        
                        m = reg.exec(v);
                        if (m)
                        {
                            if (m['groups'] && m['groups']['url'])
                            {
                                var url = m['groups']['url'];
                                if (server_data.hasOwnProperty(url))
                                {
                                    console.log(`Added url:${url} to be replaced with data of ${server_data[url].length} bytes length`);
                                    replaces[url] = server_data[url];                                    
                                }
                            }
                        }
                    }
                }
                
                for (let src in replaces)
                {
                    let dest = replaces[src];
                    v = v.replace(src, dest);
                }

                return old_prefilter(v);
            };
        });

        var server_data={
 "data/behaviors.csv": "\"BROKEN\",\"EPIC\",\"FAILED\",\"FEATURE\",\"PASSED\",\"SKIPPED\",\"STORY\",\"UNKNOWN\"\n\"0\",\"\",\"0\",\"登录功能\",\"1\",\"0\",\"登录成功\",\"0\"\n", 
 "data/behaviors.json": "{\"uid\":\"b1a8273437954620fa374b796ffaacdd\",\"name\":\"behaviors\",\"children\":[{\"name\":\"登录功能\",\"children\":[{\"name\":\"登录成功\",\"children\":[{\"name\":\"test_login_success[chromium]\",\"uid\":\"3024878d1be18db3\",\"parentUid\":\"2d25cc6a4af406470a88996c3fdc840d\",\"status\":\"passed\",\"time\":{\"start\":1786616114668,\"stop\":1786616129865,\"duration\":15197},\"flaky\":false,\"newFailed\":false,\"newPassed\":false,\"newBroken\":false,\"retriesCount\":0,\"retriesStatusChange\":false,\"parameters\":[\"{'browser_name': 'chromium', 'headless': False}\"],\"tags\":[]}],\"uid\":\"2d25cc6a4af406470a88996c3fdc840d\"}],\"uid\":\"76c1a89e029bf2806c0ddb06b8505b0b\"}]}", 
 "data/categories.csv": "", 
 "data/categories.json": "{\"uid\":\"4b4757e66a1912dae1a509f688f20b0f\",\"name\":\"categories\",\"children\":[]}", 
 "data/packages.json": "{\"uid\":\"83edc06c07f9ae9e47eb6dd1b683e4e2\",\"name\":\"packages\",\"children\":[{\"name\":\"test_case.test_login.test_login_success\",\"children\":[{\"name\":\"test_login_success[chromium]\",\"uid\":\"3024878d1be18db3\",\"parentUid\":\"8bff792acc7a179bafba137c294ed63e\",\"status\":\"passed\",\"time\":{\"start\":1786616114668,\"stop\":1786616129865,\"duration\":15197},\"flaky\":false,\"newFailed\":false,\"newPassed\":false,\"newBroken\":false,\"retriesCount\":0,\"retriesStatusChange\":false,\"parameters\":[\"{'browser_name': 'chromium', 'headless': False}\"],\"tags\":[]}],\"uid\":\"test_case.test_login.test_login_success\"}]}", 
 "data/suites.csv": "\"DESCRIPTION\",\"DURATION IN MS\",\"NAME\",\"PARENT SUITE\",\"START TIME\",\"STATUS\",\"STOP TIME\",\"SUB SUITE\",\"SUITE\",\"TEST CLASS\",\"TEST METHOD\"\n\"\",\"15197\",\"test_login_success[chromium]\",\"test_case.test_login\",\"Thu Aug 13 18:15:14 CST 2026\",\"passed\",\"Thu Aug 13 18:15:29 CST 2026\",\"TestLoginSuccess\",\"test_login_success\",\"\",\"\"\n", 
 "data/suites.json": "{\"uid\":\"98d3104e051c652961429bf95fa0b5d6\",\"name\":\"suites\",\"children\":[{\"name\":\"test_case.test_login\",\"children\":[{\"name\":\"test_login_success\",\"children\":[{\"name\":\"TestLoginSuccess\",\"children\":[{\"name\":\"test_login_success[chromium]\",\"uid\":\"3024878d1be18db3\",\"parentUid\":\"d7f0f938654e2eba23f1ac5361f72f0a\",\"status\":\"passed\",\"time\":{\"start\":1786616114668,\"stop\":1786616129865,\"duration\":15197},\"flaky\":false,\"newFailed\":false,\"newPassed\":false,\"newBroken\":false,\"retriesCount\":0,\"retriesStatusChange\":false,\"parameters\":[\"{'browser_name': 'chromium', 'headless': False}\"],\"tags\":[]}],\"uid\":\"d7f0f938654e2eba23f1ac5361f72f0a\"}],\"uid\":\"d9763a71a82c019758dabaf65854341f\"}],\"uid\":\"7e1d3bce57b6386af2355e8d52097604\"}]}", 
 "data/timeline.json": "{\"uid\":\"ab17fc5a4eb3bca4b216b548c7f9fcbc\",\"name\":\"timeline\",\"children\":[{\"name\":\"B-03-01\",\"children\":[{\"name\":\"28052-MainThread\",\"children\":[{\"name\":\"test_login_success[chromium]\",\"uid\":\"3024878d1be18db3\",\"parentUid\":\"b0ab8f8aa1fea33134b0ae6da9dce0dd\",\"status\":\"passed\",\"time\":{\"start\":1786616114668,\"stop\":1786616129865,\"duration\":15197},\"flaky\":false,\"newFailed\":false,\"newPassed\":false,\"newBroken\":false,\"retriesCount\":0,\"retriesStatusChange\":false,\"parameters\":[\"{'browser_name': 'chromium', 'headless': False}\"],\"tags\":[]}],\"uid\":\"b0ab8f8aa1fea33134b0ae6da9dce0dd\"}],\"uid\":\"674a7221ac71ca6a8ab910995b9f3330\"}]}", 
 "data/test-cases/3024878d1be18db3.json": "{\"uid\":\"3024878d1be18db3\",\"name\":\"test_login_success[chromium]\",\"fullName\":\"test_case.test_login.test_login_success.TestLoginSuccess#test_login_success\",\"historyId\":\"ad329a9b9ccfa0d4a4298de9dd06976d\",\"time\":{\"start\":1786616114668,\"stop\":1786616129865,\"duration\":15197},\"status\":\"passed\",\"flaky\":false,\"newFailed\":false,\"newBroken\":false,\"newPassed\":false,\"retriesCount\":0,\"retriesStatusChange\":false,\"beforeStages\":[{\"name\":\"_session_faker\",\"time\":{\"start\":1786616111899,\"stop\":1786616111964,\"duration\":65},\"status\":\"passed\",\"steps\":[],\"attachments\":[],\"parameters\":[],\"attachmentsCount\":0,\"shouldDisplayMessage\":false,\"hasContent\":false,\"attachmentStep\":false,\"stepsCount\":0},{\"name\":\"page\",\"time\":{\"start\":1786616111964,\"stop\":1786616114666,\"duration\":2702},\"status\":\"passed\",\"steps\":[],\"attachments\":[],\"parameters\":[],\"attachmentsCount\":0,\"shouldDisplayMessage\":false,\"hasContent\":false,\"attachmentStep\":false,\"stepsCount\":0}],\"testStage\":{\"status\":\"passed\",\"steps\":[{\"name\":\"执行登录：用户名='admin', 密码='macro123'\",\"time\":{\"start\":1786616114683,\"stop\":1786616119649,\"duration\":4966},\"status\":\"passed\",\"steps\":[],\"attachments\":[],\"parameters\":[{\"name\":\"username\",\"value\":\"'admin'\"},{\"name\":\"password\",\"value\":\"'macro123'\"}],\"attachmentsCount\":0,\"shouldDisplayMessage\":false,\"hasContent\":true,\"attachmentStep\":false,\"stepsCount\":0}],\"attachments\":[],\"parameters\":[],\"attachmentsCount\":0,\"shouldDisplayMessage\":false,\"hasContent\":true,\"attachmentStep\":false,\"stepsCount\":1},\"afterStages\":[{\"name\":\"page::0\",\"time\":{\"start\":1786616129866,\"stop\":1786616130568,\"duration\":702},\"status\":\"passed\",\"steps\":[],\"attachments\":[],\"parameters\":[],\"attachmentsCount\":0,\"shouldDisplayMessage\":false,\"hasContent\":false,\"attachmentStep\":false,\"stepsCount\":0}],\"labels\":[{\"name\":\"story\",\"value\":\"登录成功\"},{\"name\":\"feature\",\"value\":\"登录功能\"},{\"name\":\"parentSuite\",\"value\":\"test_case.test_login\"},{\"name\":\"suite\",\"value\":\"test_login_success\"},{\"name\":\"subSuite\",\"value\":\"TestLoginSuccess\"},{\"name\":\"host\",\"value\":\"B-03-01\"},{\"name\":\"thread\",\"value\":\"28052-MainThread\"},{\"name\":\"framework\",\"value\":\"pytest\"},{\"name\":\"language\",\"value\":\"cpython3\"},{\"name\":\"package\",\"value\":\"test_case.test_login.test_login_success\"},{\"name\":\"resultFormat\",\"value\":\"allure2\"}],\"parameters\":[{\"name\":\"page\",\"value\":\"{'browser_name': 'chromium', 'headless': False}\"}],\"links\":[],\"hidden\":false,\"retry\":false,\"extra\":{\"severity\":\"normal\",\"retries\":[],\"categories\":[],\"tags\":[]},\"source\":\"3024878d1be18db3.json\",\"parameterValues\":[\"{'browser_name': 'chromium', 'headless': False}\"]}", 
 "export/influxDbData.txt": "launch_status failed=0 1786616134000000000\nlaunch_status broken=0 1786616134000000000\nlaunch_status passed=1 1786616134000000000\nlaunch_status skipped=0 1786616134000000000\nlaunch_status unknown=0 1786616134000000000\nlaunch_time duration=15197 1786616134000000000\nlaunch_time min_duration=15197 1786616134000000000\nlaunch_time max_duration=15197 1786616134000000000\nlaunch_time sum_duration=15197 1786616134000000000\nlaunch_time start=1786616114668 1786616134000000000\nlaunch_time stop=1786616129865 1786616134000000000\nlaunch_retries retries=0 1786616134000000000\nlaunch_retries run=1 1786616134000000000\n", 
 "export/mail.html": "data:text/html;base64, PCFET0NUWVBFIGh0bWw+CjxodG1sPgo8aGVhZD4KICAgIDxtZXRhIGNoYXJzZXQ9InV0Zi04Ij4KICAgIDx0aXRsZT5BbGx1cmUgUmVwb3J0IHN1bW1hcnkgbWFpbDwvdGl0bGU+CjwvaGVhZD4KPGJvZHk+CiAgICBNYWlsIGJvZHkKPC9ib2R5Pgo8L2h0bWw+Cg==", 
 "export/prometheusData.txt": "launch_status_failed 0\nlaunch_status_broken 0\nlaunch_status_passed 1\nlaunch_status_skipped 0\nlaunch_status_unknown 0\nlaunch_time_duration 15197\nlaunch_time_min_duration 15197\nlaunch_time_max_duration 15197\nlaunch_time_sum_duration 15197\nlaunch_time_start 1786616114668\nlaunch_time_stop 1786616129865\nlaunch_retries_retries 0\nlaunch_retries_run 1\n", 
 "history/categories-trend.json": "[{\"data\":{}}]", 
 "history/duration-trend.json": "[{\"data\":{\"duration\":15197}}]", 
 "history/history-trend.json": "[{\"data\":{\"failed\":0,\"broken\":0,\"skipped\":0,\"passed\":1,\"unknown\":0,\"total\":1}}]", 
 "history/history.json": "{\"ad329a9b9ccfa0d4a4298de9dd06976d\":{\"statistic\":{\"failed\":0,\"broken\":0,\"skipped\":0,\"passed\":1,\"unknown\":0,\"total\":1},\"items\":[{\"uid\":\"3024878d1be18db3\",\"status\":\"passed\",\"time\":{\"start\":1786616114668,\"stop\":1786616129865,\"duration\":15197}}]}}", 
 "history/retry-trend.json": "[{\"data\":{\"run\":1,\"retry\":0}}]", 
 "plugin/behaviors/index.js": "'use strict';\n\nallure.api.addTranslation('en', {\n    tab: {\n        behaviors: {\n            name: 'Behaviors'\n        }\n    },\n    widget: {\n        behaviors: {\n            name: 'Features by stories',\n            showAll: 'show all'\n        }\n    }\n});\n\nallure.api.addTranslation('ru', {\n    tab: {\n        behaviors: {\n            name: 'Функциональность'\n        }\n    },\n    widget: {\n        behaviors: {\n            name: 'Функциональность',\n            showAll: 'показать все'\n        }\n    }\n});\n\nallure.api.addTranslation('zh', {\n    tab: {\n        behaviors: {\n            name: '功能'\n        }\n    },\n    widget: {\n        behaviors: {\n            name: '特性场景',\n            showAll: '显示所有'\n        }\n    }\n});\n\nallure.api.addTranslation('de', {\n    tab: {\n        behaviors: {\n            name: 'Verhalten'\n        }\n    },\n    widget: {\n        behaviors: {\n            name: 'Features nach Stories',\n            showAll: 'Zeige alle'\n        }\n    }\n});\n\nallure.api.addTranslation('nl', {\n    tab: {\n        behaviors: {\n            name: 'Functionaliteit'\n        }\n    },\n    widget: {\n        behaviors: {\n            name: 'Features en story’s',\n            showAll: 'Toon alle'\n        }\n    }\n});\n\nallure.api.addTranslation('he', {\n    tab: {\n        behaviors: {\n            name: 'התנהגויות'\n        }\n    },\n    widget: {\n        behaviors: {\n            name: 'תכונות לפי סיפורי משתמש',\n            showAll: 'הצג הכול'\n        }\n    }\n});\n\nallure.api.addTranslation('br', {\n    tab: {\n        behaviors: {\n            name: 'Comportamentos'\n        }\n    },\n    widget: {\n        behaviors: {\n            name: 'Funcionalidades por história',\n            showAll: 'Mostrar tudo'\n        }\n    }\n});\n\nallure.api.addTranslation('ja', {\n    tab: {\n        behaviors: {\n            name: '振る舞い'\n        }\n    },\n    widget: {\n        behaviors: {\n            name: 'ストーリー別の機能',\n            showAll: '全て表示'\n        }\n    }\n});\n\nallure.api.addTranslation('es', {\n    tab: {\n        behaviors: {\n            name: 'Funcionalidades'\n        }\n    },\n    widget: {\n        behaviors: {\n            name: 'Funcionalidades por Historias de Usuario',\n            showAll: 'mostrar todo'\n        }\n    }\n});\n\nallure.api.addTranslation('kr', {\n    tab: {\n        behaviors: {\n            name: '동작'\n        }\n    },\n    widget: {\n        behaviors: {\n            name: '스토리별 기능',\n            showAll: '전체 보기'\n        }\n    }\n});\n\nallure.api.addTranslation('fr', {\n    tab: {\n        behaviors: {\n            name: 'Comportements'\n        }\n    },\n    widget: {\n        behaviors: {\n            name: 'Thèmes par histoires',\n            showAll: 'Montrer tout'\n        }\n    }\n});\n\nallure.api.addTranslation('pl', {\n    tab: {\n        behaviors: {\n            name: 'Zachowania'\n        }\n    },\n    widget: {\n        behaviors: {\n            name: 'Funkcje według historii',\n            showAll: 'pokaż wszystko'\n        }\n    }\n});\n\nallure.api.addTranslation('am', {\n    tab: {\n        behaviors: {\n            name: 'Վարքագծեր'\n        }\n    },\n    widget: {\n        behaviors: {\n            name: 'Ֆիչրները ըստ պատմությունների',\n            showAll: 'ցույց տալ բոլորը'\n        }\n    }\n});\n\nallure.api.addTranslation('az', {\n    tab: {\n        behaviors: {\n            name: 'Davranışlar'\n        }\n    },\n    widget: {\n        behaviors: {\n            name: 'Hekayələr üzrə xüsusiyyətlər',\n            showAll: 'hamısını göstər'\n        }\n    }\n});\n\nallure.api.addTranslation('sv', {\n    tab: {\n        behaviors: {\n            name: 'Beteenden'\n        }\n    },\n    widget: {\n        behaviors: {\n            name: 'Funktioner efter user stories',\n            showAll: 'visa allt'\n        }\n    }\n});\n\nallure.api.addTranslation('isv', {\n    tab: {\n        behaviors: {\n            name: 'Funkcionalnost',\n        }\n    },\n    widget: {\n        behaviors: {\n            name: 'Funkcionalnost',\n            showAll: 'pokaži vsěčto',\n        }\n    }\n});\n\nallure.api.addTranslation('ka', {\n    tab: {\n        behaviors: {\n            name: 'ფუნქციონალი',\n        }\n    },\n    widget: {\n        behaviors: {\n            name: 'ფუნქციონალი',\n            showAll: 'ყველას ჩვენება',\n        }\n    }\n});\n\nallure.api.addTranslation('it', {\n    tab: {\n        behaviors: {\n            name: 'Comportamenti'\n        }\n    },\n    widget: {\n        behaviors: {\n            name: 'Funzionalità per storie',\n            showAll: 'Mostra tutto'\n        }\n    }\n});\n\nallure.api.addTab('behaviors', {\n    title: 'tab.behaviors.name', icon: 'fa fa-list',\n    route: 'behaviors(/)(:testGroup)(/)(:testResult)(/)(:testResultTab)(/)',\n    onEnter: (function (testGroup, testResult, testResultTab) {\n        return new allure.components.TreeLayout({\n            testGroup: testGroup,\n            testResult: testResult,\n            testResultTab: testResultTab,\n            tabName: 'tab.behaviors.name',\n            baseUrl: 'behaviors',\n            url: 'data/behaviors.json',\n            csvUrl: 'data/behaviors.csv'\n        });\n    })\n});\n\nallure.api.addWidget('widgets', 'behaviors', allure.components.WidgetStatusView.extend({\n    rowTag: 'a',\n    title: 'widget.behaviors.name',\n    baseUrl: 'behaviors',\n    showLinks: true\n}));\n", 
 "plugin/packages/index.js": "'use strict';\n\nallure.api.addTranslation('en', {\n    tab: {\n        packages: {\n            name: 'Packages'\n        }\n    }\n});\n\nallure.api.addTranslation('ru', {\n    tab: {\n        packages: {\n            name: 'Пакеты'\n        }\n    }\n});\n\nallure.api.addTranslation('zh', {\n    tab: {\n        packages: {\n            name: '包'\n        }\n    }\n});\n\nallure.api.addTranslation('de', {\n    tab: {\n        packages: {\n            name: 'Pakete'\n        }\n    }\n});\n\nallure.api.addTranslation('nl', {\n    tab: {\n        packages: {\n            name: 'Packages'\n        }\n    }\n});\n\nallure.api.addTranslation('he', {\n    tab: {\n        packages: {\n            name: 'חבילות'\n        }\n    }\n});\n\nallure.api.addTranslation('br', {\n    tab: {\n        packages: {\n            name: 'Pacotes'\n        }\n    }\n});\n\nallure.api.addTranslation('ja', {\n    tab: {\n        packages: {\n            name: 'パッケージ'\n        }\n    }\n});\n\nallure.api.addTranslation('es', {\n    tab: {\n        packages: {\n            name: 'Paquetes'\n        }\n    }\n});\n\nallure.api.addTranslation('kr', {\n    tab: {\n        packages: {\n            name: '패키지'\n        }\n    }\n});\n\nallure.api.addTranslation('fr', {\n    tab: {\n        packages: {\n            name: 'Paquets'\n        }\n    }\n});\n\nallure.api.addTranslation('pl', {\n    tab: {\n        packages: {\n            name: 'Pakiety'\n        }\n    }\n});\n\nallure.api.addTranslation('am', {\n    tab: {\n        packages: {\n            name: 'Փաթեթներ'\n        }\n    }\n});\n\nallure.api.addTranslation('az', {\n    tab: {\n        packages: {\n            name: 'Paketlər'\n        }\n    }\n});\n\nallure.api.addTranslation('sv', {\n    tab: {\n        packages: {\n            name: 'Paket'\n        }\n    }\n});\n\nallure.api.addTranslation('isv', {\n    tab: {\n        packages: {\n            name: 'Pakety'\n        }\n    }\n});\n\nallure.api.addTranslation('ka', {\n    tab: {\n        packages: {\n            name: 'პაკეტები'\n        }\n    }\n});\n\nallure.api.addTranslation('it', {\n    tab: {\n        packages: {\n            name: 'Pacchetti'\n        }\n    }\n});\n\nallure.api.addTab('packages', {\n    title: 'tab.packages.name', icon: 'fa fa-align-left',\n    route: 'packages(/)(:testGroup)(/)(:testResult)(/)(:testResultTab)(/)',\n    onEnter: (function (testGroup, testResult, testResultTab) {\n        return new allure.components.TreeLayout({\n            testGroup: testGroup,\n            testResult: testResult,\n            testResultTab: testResultTab,\n            tabName: 'tab.packages.name',\n            baseUrl: 'packages',\n            url: 'data/packages.json'\n        });\n    })\n});\n", 
 "plugin/screen-diff/index.js": "(function () {\n    var settings = allure.getPluginSettings('screen-diff', { diffType: 'diff' });\n\n    function renderImage(src) {\n        return (\n            '&lt;div class=\"screen-diff__container\"&gt;' +\n            '&lt;img class=\"screen-diff__image\" src=\"' +\n            src +\n            '\"&gt;' +\n            '&lt;/div&gt;'\n        );\n    }\n\n    function findImage(data, name) {\n        if (data.testStage && data.testStage.attachments) {\n            var matchedImage = data.testStage.attachments.filter(function (attachment) {\n                return attachment.name === name;\n            })[0];\n            if (matchedImage) {\n                return 'data/attachments/' + matchedImage.source;\n            }\n        }\n        return null;\n    }\n\n    function renderDiffContent(type, diffImage, actualImage, expectedImage) {\n        if (type === 'diff') {\n            if (diffImage) {\n                return renderImage(diffImage);\n            }\n        }\n        if (type === 'overlay' && expectedImage) {\n            return (\n                '&lt;div class=\"screen-diff__overlay screen-diff__container\"&gt;' +\n                '&lt;img class=\"screen-diff__image\" src=\"' +\n                expectedImage +\n                '\"&gt;' +\n                '&lt;div class=\"screen-diff__image-over\"&gt;' +\n                '&lt;img class=\"screen-diff__image\" src=\"' +\n                actualImage +\n                '\"&gt;' +\n                '&lt;/div&gt;' +\n                '&lt;/div&gt;'\n            );\n        }\n        if (actualImage) {\n            return renderImage(actualImage);\n        }\n        return 'No diff data provided';\n    }\n\n    var TestResultView = Backbone.Marionette.View.extend({\n        regions: {\n            subView: '.screen-diff-view',\n        },\n        template: function () {\n            return '&lt;div class=\"screen-diff-view\"&gt;&lt;/div&gt;';\n        },\n        onRender: function () {\n            var data = this.model.toJSON();\n            var testType = data.labels.filter(function (label) {\n                return label.name === 'testType';\n            })[0];\n            var diffImage = findImage(data, 'diff');\n            var actualImage = findImage(data, 'actual');\n            var expectedImage = findImage(data, 'expected');\n            if (!testType || testType.value !== 'screenshotDiff') {\n                return;\n            }\n            this.showChildView(\n                'subView',\n                new ScreenDiffView({\n                    diffImage: diffImage,\n                    actualImage: actualImage,\n                    expectedImage: expectedImage,\n                }),\n            );\n        },\n    });\n    var ErrorView = Backbone.Marionette.View.extend({\n        templateContext: function () {\n            return this.options;\n        },\n        template: function (data) {\n            return '&lt;pre class=\"screen-diff-error\"&gt;' + data.error + '&lt;/pre&gt;';\n        },\n    });\n    var AttachmentView = Backbone.Marionette.View.extend({\n        regions: {\n            subView: '.screen-diff-view',\n        },\n        template: function () {\n            return '&lt;div class=\"screen-diff-view\"&gt;&lt;/div&gt;';\n        },\n        onRender: function () {\n            jQuery\n                .getJSON(this.options.sourceUrl)\n                .then(this.renderScreenDiffView.bind(this), this.renderErrorView.bind(this));\n        },\n        renderErrorView: function (error) {\n            console.log(error);\n            this.showChildView(\n                'subView',\n                new ErrorView({\n                    error: error.statusText,\n                }),\n            );\n        },\n        renderScreenDiffView: function (data) {\n            this.showChildView(\n                'subView',\n                new ScreenDiffView({\n                    diffImage: data.diff,\n                    actualImage: data.actual,\n                    expectedImage: data.expected,\n                }),\n            );\n        },\n    });\n\n    var ScreenDiffView = Backbone.Marionette.View.extend({\n        className: 'pane__section',\n        events: function () {\n            return {\n                ['click [name=\"screen-diff-type-' + this.cid + '\"]']: 'onDiffTypeChange',\n                'mousemove .screen-diff__overlay': 'onOverlayMove',\n            };\n        },\n        initialize: function (options) {\n            this.diffImage = options.diffImage;\n            this.actualImage = options.actualImage;\n            this.expectedImage = options.expectedImage;\n            this.radioName = 'screen-diff-type-' + this.cid;\n        },\n        templateContext: function () {\n            return {\n                diffType: settings.get('diffType'),\n                diffImage: this.diffImage,\n                actualImage: this.actualImage,\n                expectedImage: this.expectedImage,\n                radioName: this.radioName,\n            };\n        },\n        template: function (data) {\n            if (!data.diffImage && !data.actualImage && !data.expectedImage) {\n                return '';\n            }\n\n            return (\n                '&lt;h3 class=\"pane__section-title\"&gt;Screen Diff&lt;/h3&gt;' +\n                '&lt;div class=\"screen-diff__content\"&gt;' +\n                '&lt;div class=\"screen-diff__switchers\"&gt;' +\n                '&lt;label&gt;&lt;input type=\"radio\" name=\"' +\n                data.radioName +\n                '\" value=\"diff\"&gt; Show diff&lt;/label&gt;' +\n                '&lt;label&gt;&lt;input type=\"radio\" name=\"' +\n                data.radioName +\n                '\" value=\"overlay\"&gt; Show overlay&lt;/label&gt;' +\n                '&lt;/div&gt;' +\n                renderDiffContent(\n                    data.diffType,\n                    data.diffImage,\n                    data.actualImage,\n                    data.expectedImage,\n                ) +\n                '&lt;/div&gt;'\n            );\n        },\n        adjustImageSize: function (event) {\n            var overImage = this.$(event.target);\n            overImage.width(overImage.width());\n        },\n        onRender: function () {\n            const diffType = settings.get('diffType');\n            this.$('[name=\"' + this.radioName + '\"][value=\"' + diffType + '\"]').prop(\n                'checked',\n                true,\n            );\n            if (diffType === 'overlay') {\n                this.$('.screen-diff__image-over img').on('load', this.adjustImageSize.bind(this));\n            }\n        },\n        onOverlayMove: function (event) {\n            var pageX = event.pageX;\n            var containerScroll = this.$('.screen-diff__container').scrollLeft();\n            var elementX = event.currentTarget.getBoundingClientRect().left;\n            var delta = pageX - elementX + containerScroll;\n            this.$('.screen-diff__image-over').width(delta);\n        },\n        onDiffTypeChange: function (event) {\n            settings.save('diffType', event.target.value);\n            this.render();\n        },\n    });\n    allure.api.addTestResultBlock(TestResultView, { position: 'before' });\n    allure.api.addAttachmentViewer('application/vnd.allure.image.diff', {\n        View: AttachmentView,\n        icon: 'fa fa-exchange',\n    });\n})();\n", 
 "plugin/screen-diff/styles.css": ".screen-diff__switchers {\n  margin-bottom: 1em;\n}\n\n.screen-diff__switchers label + label {\n  margin-left: 1em;\n}\n\n.screen-diff__overlay {\n  position: relative;\n  cursor: col-resize;\n}\n\n.screen-diff__container {\n  overflow-x: auto;\n}\n\n.screen-diff__image-over {\n  top: 0;\n  left: 0;\n  bottom: 0;\n  background: #fff;\n  position: absolute;\n  overflow: hidden;\n  box-shadow: 2px 0 1px -1px #aaa;\n}\n\n.screen-diff-error {\n  color: #fd5a3e;\n}\n", 
 "widgets/behaviors.json": "{\"total\":1,\"items\":[{\"uid\":\"76c1a89e029bf2806c0ddb06b8505b0b\",\"name\":\"登录功能\",\"statistic\":{\"failed\":0,\"broken\":0,\"skipped\":0,\"passed\":1,\"unknown\":0,\"total\":1}}]}", 
 "widgets/categories-trend.json": "[{\"data\":{}}]", 
 "widgets/categories.json": "{\"total\":0,\"items\":[]}", 
 "widgets/duration-trend.json": "[{\"data\":{\"duration\":15197}}]", 
 "widgets/duration.json": "[{\"uid\":\"3024878d1be18db3\",\"name\":\"test_login_success[chromium]\",\"time\":{\"start\":1786616114668,\"stop\":1786616129865,\"duration\":15197},\"status\":\"passed\",\"severity\":\"normal\"}]", 
 "widgets/environment.json": "[]", 
 "widgets/executors.json": "[]", 
 "widgets/history-trend.json": "[{\"data\":{\"failed\":0,\"broken\":0,\"skipped\":0,\"passed\":1,\"unknown\":0,\"total\":1}}]", 
 "widgets/launch.json": "[]", 
 "widgets/retry-trend.json": "[{\"data\":{\"run\":1,\"retry\":0}}]", 
 "widgets/severity.json": "[{\"uid\":\"3024878d1be18db3\",\"name\":\"test_login_success[chromium]\",\"time\":{\"start\":1786616114668,\"stop\":1786616129865,\"duration\":15197},\"status\":\"passed\",\"severity\":\"normal\"}]", 
 "widgets/status-chart.json": "[{\"uid\":\"3024878d1be18db3\",\"name\":\"test_login_success[chromium]\",\"time\":{\"start\":1786616114668,\"stop\":1786616129865,\"duration\":15197},\"status\":\"passed\",\"severity\":\"normal\"}]", 
 "widgets/suites.json": "{\"total\":1,\"items\":[{\"uid\":\"7e1d3bce57b6386af2355e8d52097604\",\"name\":\"test_case.test_login\",\"statistic\":{\"failed\":0,\"broken\":0,\"skipped\":0,\"passed\":1,\"unknown\":0,\"total\":1}}]}", 
 "widgets/summary.json": "{\"reportName\":\"Allure Report\",\"testRuns\":[],\"statistic\":{\"failed\":0,\"broken\":0,\"skipped\":0,\"passed\":1,\"unknown\":0,\"total\":1},\"time\":{\"start\":1786616114668,\"stop\":1786616129865,\"duration\":15197,\"minDuration\":15197,\"maxDuration\":15197,\"sumDuration\":15197}}", 
};
    var server = sinon.fakeServer.create();

                server.respondWith("GET", "data/behaviors.csv", [
                      200, { "Content-Type": "text/csv" }, server_data["data/behaviors.csv"],
                ]);
            
                server.respondWith("GET", "data/behaviors.json", [
                      200, { "Content-Type": "application/json" }, server_data["data/behaviors.json"],
                ]);
            
                server.respondWith("GET", "data/categories.csv", [
                      200, { "Content-Type": "text/csv" }, server_data["data/categories.csv"],
                ]);
            
                server.respondWith("GET", "data/categories.json", [
                      200, { "Content-Type": "application/json" }, server_data["data/categories.json"],
                ]);
            
                server.respondWith("GET", "data/packages.json", [
                      200, { "Content-Type": "application/json" }, server_data["data/packages.json"],
                ]);
            
                server.respondWith("GET", "data/suites.csv", [
                      200, { "Content-Type": "text/csv" }, server_data["data/suites.csv"],
                ]);
            
                server.respondWith("GET", "data/suites.json", [
                      200, { "Content-Type": "application/json" }, server_data["data/suites.json"],
                ]);
            
                server.respondWith("GET", "data/timeline.json", [
                      200, { "Content-Type": "application/json" }, server_data["data/timeline.json"],
                ]);
            
                server.respondWith("GET", "data/test-cases/3024878d1be18db3.json", [
                      200, { "Content-Type": "application/json" }, server_data["data/test-cases/3024878d1be18db3.json"],
                ]);
            
                server.respondWith("GET", "export/influxDbData.txt", [
                      200, { "Content-Type": "text/plain;charset=UTF-8" }, server_data["export/influxDbData.txt"],
                ]);
            
                server.respondWith("GET", "export/mail.html", [
                      200, { "Content-Type": "text/html" }, server_data["export/mail.html"],
                ]);
            
                server.respondWith("GET", "export/prometheusData.txt", [
                      200, { "Content-Type": "text/plain;charset=UTF-8" }, server_data["export/prometheusData.txt"],
                ]);
            
                server.respondWith("GET", "history/categories-trend.json", [
                      200, { "Content-Type": "application/json" }, server_data["history/categories-trend.json"],
                ]);
            
                server.respondWith("GET", "history/duration-trend.json", [
                      200, { "Content-Type": "application/json" }, server_data["history/duration-trend.json"],
                ]);
            
                server.respondWith("GET", "history/history-trend.json", [
                      200, { "Content-Type": "application/json" }, server_data["history/history-trend.json"],
                ]);
            
                server.respondWith("GET", "history/history.json", [
                      200, { "Content-Type": "application/json" }, server_data["history/history.json"],
                ]);
            
                server.respondWith("GET", "history/retry-trend.json", [
                      200, { "Content-Type": "application/json" }, server_data["history/retry-trend.json"],
                ]);
            
                server.respondWith("GET", "plugin/behaviors/index.js", [
                      200, { "Content-Type": "application/javascript" }, server_data["plugin/behaviors/index.js"],
                ]);
            
                server.respondWith("GET", "plugin/packages/index.js", [
                      200, { "Content-Type": "application/javascript" }, server_data["plugin/packages/index.js"],
                ]);
            
                server.respondWith("GET", "plugin/screen-diff/index.js", [
                      200, { "Content-Type": "application/javascript" }, server_data["plugin/screen-diff/index.js"],
                ]);
            
                server.respondWith("GET", "plugin/screen-diff/styles.css", [
                      200, { "Content-Type": "text/css" }, server_data["plugin/screen-diff/styles.css"],
                ]);
            
                server.respondWith("GET", "widgets/behaviors.json", [
                      200, { "Content-Type": "application/json" }, server_data["widgets/behaviors.json"],
                ]);
            
                server.respondWith("GET", "widgets/categories-trend.json", [
                      200, { "Content-Type": "application/json" }, server_data["widgets/categories-trend.json"],
                ]);
            
                server.respondWith("GET", "widgets/categories.json", [
                      200, { "Content-Type": "application/json" }, server_data["widgets/categories.json"],
                ]);
            
                server.respondWith("GET", "widgets/duration-trend.json", [
                      200, { "Content-Type": "application/json" }, server_data["widgets/duration-trend.json"],
                ]);
            
                server.respondWith("GET", "widgets/duration.json", [
                      200, { "Content-Type": "application/json" }, server_data["widgets/duration.json"],
                ]);
            
                server.respondWith("GET", "widgets/environment.json", [
                      200, { "Content-Type": "application/json" }, server_data["widgets/environment.json"],
                ]);
            
                server.respondWith("GET", "widgets/executors.json", [
                      200, { "Content-Type": "application/json" }, server_data["widgets/executors.json"],
                ]);
            
                server.respondWith("GET", "widgets/history-trend.json", [
                      200, { "Content-Type": "application/json" }, server_data["widgets/history-trend.json"],
                ]);
            
                server.respondWith("GET", "widgets/launch.json", [
                      200, { "Content-Type": "application/json" }, server_data["widgets/launch.json"],
                ]);
            
                server.respondWith("GET", "widgets/retry-trend.json", [
                      200, { "Content-Type": "application/json" }, server_data["widgets/retry-trend.json"],
                ]);
            
                server.respondWith("GET", "widgets/severity.json", [
                      200, { "Content-Type": "application/json" }, server_data["widgets/severity.json"],
                ]);
            
                server.respondWith("GET", "widgets/status-chart.json", [
                      200, { "Content-Type": "application/json" }, server_data["widgets/status-chart.json"],
                ]);
            
                server.respondWith("GET", "widgets/suites.json", [
                      200, { "Content-Type": "application/json" }, server_data["widgets/suites.json"],
                ]);
            
                server.respondWith("GET", "widgets/summary.json", [
                      200, { "Content-Type": "application/json" }, server_data["widgets/summary.json"],
                ]);
            server.autoRespond = true;