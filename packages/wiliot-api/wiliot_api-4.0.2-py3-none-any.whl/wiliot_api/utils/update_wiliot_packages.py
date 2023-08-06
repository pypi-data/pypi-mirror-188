#  """
#    Copyright (c) 2016- 2022, Wiliot Ltd. All rights reserved.
#
#    Redistribution and use of the Software in source and binary forms, with or without modification,
#     are permitted provided that the following conditions are met:
#
#       1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#       2. Redistributions in binary form, except as used in conjunction with
#       Wiliot's Pixel in a product or a Software update for such product, must reproduce
#       the above copyright notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the distribution.
#
#       3. Neither the name nor logo of Wiliot, nor the names of the Software's contributors,
#       may be used to endorse or promote products or services derived from this Software,
#       without specific prior written permission.
#
#       4. This Software, with or without modification, must only be used in conjunction
#       with Wiliot's Pixel or with Wiliot's cloud service.
#
#       5. If any Software is provided in binary form under this license, you must not
#       do any of the following:
#       (a) modify, adapt, translate, or create a derivative work of the Software; or
#       (b) reverse engineer, decompile, disassemble, decrypt, or otherwise attempt to
#       discover the source code or non-literal aspects (such as the underlying structure,
#       sequence, organization, ideas, or algorithms) of the Software.
#
#       6. If you create a derivative work and/or improvement of any Software, you hereby
#       irrevocably grant each of Wiliot and its corporate affiliates a worldwide, non-exclusive,
#       royalty-free, fully paid-up, perpetual, irrevocable, assignable, sublicensable
#       right and license to reproduce, use, make, have made, import, distribute, sell,
#       offer for sale, create derivative works of, modify, translate, publicly perform
#       and display, and otherwise commercially exploit such derivative works and improvements
#       (as applicable) in conjunction with Wiliot's products and services.
#
#       7. You represent and warrant that you are not a resident of (and will not use the
#       Software in) a country that the U.S. government has embargoed for use of the Software,
#       nor are you named on the U.S. Treasury Department’s list of Specially Designated
#       Nationals or any other applicable trade sanctioning regulations of any jurisdiction.
#       You must not transfer, export, re-export, import, re-import or divert the Software
#       in violation of any export or re-export control laws and regulations (such as the
#       United States' ITAR, EAR, and OFAC regulations), as well as any applicable import
#       and use restrictions, all as then in effect
#
#     THIS SOFTWARE IS PROVIDED BY WILIOT "AS IS" AND "AS AVAILABLE", AND ANY EXPRESS
#     OR IMPLIED WARRANTIES OR CONDITIONS, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED
#     WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, NONINFRINGEMENT,
#     QUIET POSSESSION, FITNESS FOR A PARTICULAR PURPOSE, AND TITLE, ARE DISCLAIMED.
#     IN NO EVENT SHALL WILIOT, ANY OF ITS CORPORATE AFFILIATES OR LICENSORS, AND/OR
#     ANY CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
#     OR CONSEQUENTIAL DAMAGES, FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES,
#     FOR ANY LOSS OF USE OR DATA OR BUSINESS INTERRUPTION, AND/OR FOR ANY ECONOMIC LOSS
#     (SUCH AS LOST PROFITS, REVENUE, ANTICIPATED SAVINGS). THE FOREGOING SHALL APPLY:
#     (A) HOWEVER CAUSED AND REGARDLESS OF THE THEORY OR BASIS LIABILITY, WHETHER IN
#     CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE);
#     (B) EVEN IF ANYONE IS ADVISED OF THE POSSIBILITY OF ANY DAMAGES, LOSSES, OR COSTS; AND
#     (C) EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.
#  """
from os import popen
from sys import platform
from enum import Enum


class WiliotPackages(Enum):
    CLOUD = ['pywiliot-api']
    CORE = ['pywiliot-core', 'pywiliot-api']
    TOOLS = ['pywiliot-tools', 'pywiliot-core', 'pywiliot-api']
    DEPLOYMENT = ['pywiliot-deployment-tools', 'pywiliot-tools', 'pywiliot-core', 'pywiliot-api']
    TESTERS = ['pywiliot-testers', 'pywiliot-tools', 'pywiliot-core', 'pywiliot-api']


def update_internal_wiliot_packages(wiliot_repo=WiliotPackages.CLOUD, branch_name='master', username=''):
    # check platform command prefix
    commandPrefix = ''
    if platform == "darwin":
        # OS X
        commandPrefix = '/usr/local/bin/'
    # install pywiliot and requirements:
    # update dependencies
    print("update pip:")
    p = popen(commandPrefix + 'pip install --upgrade pip')
    rsp = p.read()
    print(rsp)

    for repo_name in wiliot_repo.value:
        package_name = repo_name.replace('py', '')
        folder_name = package_name.replace('-', '_')
        print(f'update wiliot package: {package_name}')
        p = popen(commandPrefix + f'pip install git+ssh://git@bitbucket.org/wiliot/{repo_name}.git'
                                  f'@{branch_name}#egg={folder_name} --upgrade')
        rsp = p.read()
        print(rsp)
        if 'Successfully installed' not in rsp.split('\n')[-2]:
            print('problem with ssh key credentials. Please try to install using username and password.\n'
                  'please rerun the function with your bitbucket username and check in the readme how to extract '
                  'the "app password" from bitbucket')
            if username:
                print(f'update wiliot package (using username and password): {package_name}')
                p = popen(commandPrefix + f'pip install git+https://{username}@bitbucket.org/wiliot/{repo_name}.git'
                                          f'@{branch_name}#egg={folder_name} --upgrade')
                rsp = p.read()
                print(rsp)

        print(f'check wiliot package: {package_name}')
        p = popen(commandPrefix + f'pip show {package_name}')
        rsp = p.read()
        print(rsp)
        if 'Location' in rsp:
            req_path = rsp.split('Location: ')[-1].split('\n')[0]
            print("update dependencies:")
            p = popen(commandPrefix + f'pip install -r {req_path}\\{folder_name}\\requirements.txt')
            rsp = p.read()
            print(rsp)
    print('done installation')


if __name__ == '__main__':
    update_internal_wiliot_packages(branch_name='cleanup')
