# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oidc']

package_data = \
{'': ['*'], 'oidc': ['templates/oidc/*']}

entry_points = \
{'sentry.apps': ['oidc = oidc.apps.Config']}

setup_kwargs = {
    'name': 'sentry-auth-oidc-shib',
    'version': '1.0.0',
    'description': 'OpenID Connect authentication provider for Sentry (Shibboleth)',
    'long_description': '# OIDC Auth for Sentry (Shibboleth)\n\n\nAn SSO provider for Sentry which enables [OpenID Connect](https://openid.net/connect/) Apps authentication for Shibboleth. This is a fork of [siemens/sentry-auth-oidc](https://github.com/siemens/sentry-auth-oidc), which was also forked from [getsentry/sentry-auth-google](https://github.com/getsentry/sentry-auth-google).\n\n## Why fork, instead of adapting `siemens/sentry-auth-oidc` or `getsentry/sentry-auth-google` to work with every OIDC?\nThe maintainers have different ideas. See:\n- https://github.com/getsentry/sentry-auth-google/pull/29\n- https://github.com/getsentry/sentry/issues/5650\n- Also the fork of `siemens/sentry-auth-oidc` doesn\'t work very well with Shibboleth\n    - The scope `openid` is always returned for unauthorized users, which aren\'t in the given example entitlement `sentry-users`.\n    - For that reason the request after authorization is redirected to sentry instead of directly showing an 403 error page on the identity provider side. \n\n\n## Install\n```bash\npip install sentry-auth-oidc-shib\n```\n\n\n## Setup steps for usage with Shibboleth\n### Shibboleth\n- Configure `metadata/oidc-client.json`\n    ```json\n    {\n        "scope": "openid profile email",\n        "redirect_uris": [ \n            "https://sentry.example.com/auth/sso/" \n        ],\n        "sector_identifier_uri": "https://sentry.example.com",\n        "client_id": "<client-id>",\n        "subject_type": "pairwise",\n        "client_secret": "<client-secret>",\n        "response_types": [ \n            "code"\n        ],\n        "grant_types": [ \n            "authorization_code"\n        ]\n    }\n    ```\n- Configure `conf/intercept/context-check-intercept-config.xml`\n    ```xml\n    # Content of \n    <bean id="shibboleth.context-check.Condition" parent="shibboleth.Conditions.AND">\n        <constructor-arg>\n            <list>\n                <bean class="net.shibboleth.idp.profile.logic.SimpleAttributePredicate" p:useUnfilteredAttributes="true">\n                    <property name="attributeValueMap">\n                        <map>\n                            <entry key="oidcPermissions">\n                                <list>\n                                    <value>true</value>\n                                </list>\n                            </entry>\n                        </map>\n                    </property>\n                </bean>\n            </list>\n        </constructor-arg>\n    </bean>\n    ```\n- Configure `conf/attribute-resolver.xml`\n    ```xml\n    <AttributeDefinition xsi:type="ScriptedAttribute" id="oidcPermissions" dependencyOnly="false">\n        <InputDataConnector ref="myLDAP" attributeNames="eduPersonEntitlement"/>\n        <Script><![CDATA[\n            logger = Java.type("org.slf4j.LoggerFactory").getLogger("edu.internet2.middleware.shibboleth.resolver.Script.eduPersonPrincipalNameSource");\n\n            // Get attribute to add\n            peerEntityId = profileContext.getSubcontext("net.shibboleth.idp.profile.context.RelyingPartyContext").getRelyingPartyId();\n\n            if (peerEntityId.equals("sentry.example.com") \n                    && eduPersonEntitlement.getValues().contains("urn:mace:example.com:permission:shibboleth:sentry-users")){ \n                logger.info("User can successfully login to " + peerEntityId);\n                oidcPermissions.getValues().add("true");\n            }\t\n        ]]>\n        </Script>\n    </AttributeDefinition>\n    ```\n- Configure `conf/relying-party.xml`\n    ```xml\n    <bean parent="RelyingPartyByName" c:relyingPartyIds="sentry.example.com">\n        <property name="profileConfigurations">\n        <list>\n            <bean parent="OIDC.SSO" p:postAuthenticationFlows="#{ {\'context-check\'} }"/>\n            <ref bean="OIDC.UserInfo" />\n        </list>\n        </property>\n    </bean>\n    ```\n\n### Sentry\n- Configure `sentry/sentry.conf.py`\n    ```python\n    OIDC_CLIENT_ID = "<client-id>"\n    OIDC_CLIENT_SECRET = "<client-secret>"\n    OIDC_SCOPE = "openid profile email"\n    OIDC_DOMAIN = "https://shibboleth.example.com"\n    ```\n- Configure `sentry/enhance-image.sh`\n    ```bash\n    pip install sentry-auth-oidc-shib\n    ```',
    'author': 'Michael Fuchs',
    'author_email': 'michael.fuchs@hm.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1',
}


setup(**setup_kwargs)
