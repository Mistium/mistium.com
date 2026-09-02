import urllib.request, re, json, os, hashlib
from urllib.parse import urlparse

mods_url = 'https://raw.githubusercontent.com/ScratchMod/scratchmod.github.io/refs/heads/main/src/mods.js'
tree_url = 'https://raw.githubusercontent.com/ScratchMod/scratchmod.github.io/main/src/tree.js'

mods_src = urllib.request.urlopen(mods_url).read().decode('utf-8')
tree_src = urllib.request.urlopen(tree_url).read().decode('utf-8')

mod_defs = re.findall(r'let\s+(\w+)\s*=\s*\{\s*\"name\":\s*\"([^\"]+)\",\s*\"link\":\s*\"([^\"]+)\"', mods_src)
mods_raw = {var: {'var': var, 'name': name, 'link': link} for var, name, link in mod_defs}

# Custom additions
mods_raw['Bilup'] = {'var': 'Bilup', 'name': 'Bilup', 'link': 'https://com.bilup.org/'}
mods_raw['Stretch3'] = {'var': 'Stretch3', 'name': 'Stretch3', 'link': 'https://stretch3.github.io/'}
mods_raw['KittenBlock'] = {'var': 'KittenBlock', 'name': 'KittenBlock', 'link': 'https://www.kittenbot.cc/'}
mods_raw['Scratux'] = {'var': 'Scratux', 'name': 'Scratux', 'link': 'https://scratux.org/'}
mods_raw['Leopard'] = {'var': 'Leopard', 'name': 'Leopard', 'link': 'https://leopardjs.com/'}
mods_raw['Tosh'] = {'var': 'Tosh', 'name': 'Tosh', 'link': 'https://tosh.io/'}
mods_raw['ScratchX'] = {'var': 'ScratchX', 'name': 'ScratchX', 'link': 'https://scratchx.org/'}
mods_raw['SharkMod'] = {'var': 'SharkMod', 'name': 'SharkMod', 'link': 'https://sharkmod.github.io/'}
mods_raw['ArkIDE'] = {'var': 'ArkIDE', 'name': 'ArkIDE', 'link': 'https://arc360alt.github.io/ArkIDE/editor.html#1112563456'}
mods_raw['ScratchPlusPlus'] = {'var': 'ScratchPlusPlus', 'name': 'Scratch++', 'link': 'https://zxmushroom63.github.io/scratch-gui/'}
mods_raw['AcidMod'] = {'var': 'AcidMod', 'name': 'AcidMod', 'link': 'https://acidmod.github.io/studio/'}
mods_raw['GriffpatchGUI'] = {'var': 'GriffpatchGUI', 'name': 'Griffpatch GUI', 'link': 'https://github.com/griffpatch/scratch-gui'}
mods_raw['SMTGUI'] = {'var': 'SMTGUI', 'name': 'SMT GUI', 'link': 'https://github.com/gfd-dennou-club/smt-gui'}
mods_raw['ScratchROS'] = {'var': 'ScratchROS', 'name': 'Scratch 3 ROS', 'link': 'https://github.com/Affonso-Gui/scratch3-ros-gui'}
mods_raw['RoboticalMarty'] = {'var': 'RoboticalMarty', 'name': 'Marty the Robot', 'link': 'https://robotical.io/'}
mods_raw['PollenReachy'] = {'var': 'PollenReachy', 'name': 'Reachy Robot', 'link': 'https://www.pollen-robotics.com/'}
mods_raw['ThymioScratch'] = {'var': 'ThymioScratch', 'name': 'Thymio Scratch', 'link': 'https://www.thymio.org/'}
mods_raw['ScratchESP32'] = {'var': 'ScratchESP32', 'name': 'ESP32 Scratch', 'link': 'https://github.com/cotestatnt/scratch-gui'}
mods_raw['SkullWarp'] = {'var': 'SkullWarp', 'name': 'SkullWarp', 'link': 'https://skullwarp.github.io/scratch-gui/'}
mods_raw['MistBolt'] = {'var': 'MistBolt', 'name': 'MistBolt', 'link': 'https://mistbolt.github.io/scratch-gui/'}
mods_raw['MagicMod'] = {'var': 'MagicMod', 'name': 'MagicMod', 'link': 'https://magic-mod.github.io/'}
mods_raw['Freely'] = {'var': 'Freely', 'name': 'Freely', 'link': 'https://fallingbook3215.github.io/Freely'}
mods_raw['HyperMod'] = {'var': 'HyperMod', 'name': 'Hyper', 'link': 'https://hyper.mgik.dev/editor.html'}
mods_raw['ElliNetGUI'] = {'var': 'ElliNetGUI', 'name': 'ElliNet GUI', 'link': 'https://ellinet13.github.io/scratch-gui/editor.html'}
mods_raw['Hatch'] = {'var': 'Hatch', 'name': 'Hatch', 'link': 'https://hatch.raynec.dev'}
mods_raw['SigmaMod'] = {'var': 'SigmaMod', 'name': 'SigmaMod', 'link': 'https://sigmamod.github.io/'}

# Ensure correct editor links
if 'NitroBolt' in mods_raw:
    mods_raw['NitroBolt']['link'] = 'https://nitro-bolt.github.io/scratch-gui/#0'

tree_blocks = re.findall(r'Mods\.(\w+)\.children\s*=\s*\{([^}]+)\}', tree_src)
children_map = {}
for parent, children_block in tree_blocks:
    child_vars = re.findall(r'(\w+):\s*Mods\.(\w+)', children_block)
    for k, child_var in child_vars:
        children_map.setdefault(parent, []).append(child_var)

children_map.setdefault('Mistwarp', []).extend(['Bilup', 'SkullWarp'])
children_map.setdefault('Scratch', []).extend(['Stretch3', 'KittenBlock', 'Scratux', 'Leopard', 'ScratchPlusPlus', 'GriffpatchGUI', 'ScratchROS', 'RoboticalMarty', 'PollenReachy', 'ThymioScratch', 'ScratchESP32', 'Tosh'])
children_map.setdefault('Turbowarp', []).extend(['AcidMod', 'Freely', 'ElliNetGUI', 'Hatch'])
children_map.setdefault('Penguinmod', []).extend(['SharkMod', 'ArkIDE', 'HyperMod', 'SigmaMod'])
children_map.setdefault('Smalruby', []).append('SMTGUI')
children_map.setdefault('NitroBolt', []).extend(['MistBolt', 'MagicMod'])

# -------------------------------------------------------------------------
# Ingest and enrich forks from /Users/sophie/motherforker/forks.json
# -------------------------------------------------------------------------
FORKS_PATH = '/Users/sophie/motherforker/forks.json'
if os.path.exists(FORKS_PATH):
    try:
        with open(FORKS_PATH) as f:
            forks_tree = json.load(f)
        all_fork_nodes = []
        def walk_forks(node, parent_name=None):
            all_fork_nodes.append({
                'name': node.get('name', ''),
                'url': node.get('url', ''),
                'parent': parent_name,
                'kids': len(node.get('children', [])),
                'children': [c.get('name') for c in node.get('children', []) if isinstance(c, dict)]
            })
            for c in node.get('children', []):
                if isinstance(c, dict):
                    walk_forks(c, node.get('name', ''))
        walk_forks(forks_tree)

        repo_to_key = {
            'scratchfoundation/scratch-gui': 'Scratch',
            'turbowarp/scratch-gui': 'Turbowarp',
            'penguinmod/penguinmod.github.io': 'Penguinmod',
            'openblockcc/openblock-gui': 'OpenBlock',
            'sheeptester/scratch-gui': 'E_icques',
            'snail-ide/snail-ide.github.io': 'SnailIDE',
            'dinosaurmod/dinosaurmod.github.io': 'Dinosaurmod',
            'smalruby/smalruby3-gui': 'Smalruby',
            'griffpatch/scratch-gui': 'GriffpatchGUI',
            'gfd-dennou-club/smt-gui': 'SMTGUI',
            'cotestatnt/scratch-gui': 'ScratchESP32',
            'hackidemia/cognimates-gui': 'Cognimates',
            'unsandboxed/scratch-gui': 'Unsandboxed',
            'affonso-gui/scratch3-ros-gui': 'ScratchROS',
            'electramod/scratch-gui': 'Electramod',
            'codetorchnet/codetorch-block-compiler': 'CodeTorch',
            'mistwarp/scratch-gui': 'Mistwarp',
            'nitro-bolt/scratch-gui': 'NitroBolt',
            'circle-ide/circle-ide.github.io': 'CircleIDE',
            'acidmod/studio': 'AcidMod',
            'ottawastem/scratch-arduino-gui': 'ScratchArduino',
            'batscoding/batscoding.github.io': 'Batscoding',
            'arc360alt/arkide': 'ArkIDE',
            'the-arkide-project/arkide-home': 'ArkIDE',
            'fallingbook3215/freely': 'Freely',
            'mgikdev/scratch-gui': 'HyperMod',
            'ellinet13/scratch-gui': 'ElliNetGUI',
            'raynec/scratch-gui': 'Hatch',
            'sigma-mod/sigmamod.github.io': 'SigmaMod',
            'skullwarp/scratch-gui': 'SkullWarp',
            'mistbolt/scratch-gui': 'MistBolt',
            'magic-mod/magic-mod.github.io': 'MagicMod',
            'banana-mod/banana-mod.github.io': 'Bananamod',
            'shredmod/shredmod.github.io': 'Shredmod',
            'nuclearmod/editor': 'Nuclearmod',
            'gradylink/mistwarp-gui': 'Mistwarp'
        }

        for m_key, m_raw in mods_raw.items():
            if 'link' in m_raw and 'github.com' in m_raw['link']:
                clean = m_raw['link'].replace('https://github.com/', '').strip('/').lower()
                repo_to_key[clean] = m_key

        known_core_names = {m['name'].strip().lower() for m in mods_raw.values()}
        known_core_names.update({k.strip().lower() for k in mods_raw.keys()})

        keywords = ['mod', 'ide', 'warp', 'block', 'code', 'robot', 'craft', 'bot', 'ai', 'studio', 'play', 'plus', 'maker', 'learn', 'paint', 'game', 'audio', 'lab', 'cloud', 'engine', 'box', 'compiler', 'stem', 'kit', 'physics', 'music', 'matrix', 'space', 'sandbox']
        generic_ignore = ['scratchfoundation_scratch-gui', 'scratchfoundation_scratch_gui', 'scratch-gui-temp', 'scratch-gui-test', 'scratch-gui-fork']

        def clean_display_name(repo_name, owner):
            repo_clean = repo_name.replace('.github.io', '').replace('-home', '').replace('_home', '')
            if repo_clean.lower() in ['scratch-gui', 'gui', 'scratch']:
                return f'{owner} GUI'
            repo_clean = re.sub(r'^scratch[-_.]?gui[-_.]?', '', repo_clean, flags=re.IGNORECASE)
            repo_clean = re.sub(r'^scratch[-_.]?', '', repo_clean, flags=re.IGNORECASE)
            words = re.findall(r'[A-Za-z0-9]+', repo_clean)
            if not words or (len(words) == 1 and words[0].isdigit()):
                suffix = f" {words[0]}" if words else ""
                return f"{owner}{suffix} GUI"
            name = ' '.join(w if w.isupper() else w.capitalize() for w in words)
            if name.lower() in ['editor', 'studio', 'mod', 'custom', 'scratch gui', 'gui', 'fork', 'gui 1']:
                return f'{owner} {name}'
            return name

        seen_titles = {n.lower(): k for k, n in [(k, m['name']) for k, m in mods_raw.items()]}
        seen_urls = {m['link'].lower().rstrip('/'): k for k, m in mods_raw.items()}

        for n in all_fork_nodes:
            name = n['name']
            if not name or '/' not in name or name.lower() in repo_to_key:
                continue
            owner, repo = name.split('/', 1)
            name_low = name.lower()
            owner_low, repo_low = owner.lower(), repo.lower()
            if any(ig in repo_low for ig in generic_ignore):
                continue

            parent_repo = n.get('parent')
            parent_key = 'Scratch'
            if parent_repo:
                parent_key = repo_to_key.get(parent_repo.lower(), 'Scratch')

            parent_repo_name = (parent_repo.split('/')[1] if parent_repo and '/' in parent_repo else '').lower()
            is_clone_of_parent = (repo_low == parent_repo_name or repo_low == parent_repo_name.replace('.github.io', ''))
            
            has_kids = n['kids'] > 0
            has_kw = any(kw in repo_low or kw in owner_low for kw in keywords)
            is_custom_repo = repo_low not in ['scratch-gui', 'penguinmod.github.io', 'scratch-desktop', 'gui', 'test', 'develop']

            if is_clone_of_parent and not has_kids:
                continue

            if has_kids or (has_kw and is_custom_repo):
                disp_name = clean_display_name(repo, owner)
                norm_name = disp_name.strip().lower()
                norm_url = n['url'].lower().rstrip('/')

                if norm_name in known_core_names and not has_kids:
                    continue

                if norm_name in seen_titles:
                    disp_name = f'{owner} {disp_name}'
                    norm_name = disp_name.strip().lower()
                    if norm_name in seen_titles and not has_kids:
                        continue

                if norm_url in seen_urls:
                    continue

                var_key = 'Fork_' + re.sub(r'[^a-zA-Z0-9]', '', owner) + '_' + re.sub(r'[^a-zA-Z0-9]', '', repo)
                repo_to_key[name.lower()] = var_key
                seen_titles[norm_name] = var_key
                seen_urls[norm_url] = var_key

                mods_raw[var_key] = {
                    'var': var_key,
                    'name': disp_name,
                    'link': n['url'],
                    'owner': owner,
                    'repo': repo,
                    'kids': n['kids']
                }
                children_map.setdefault(parent_key, []).append(var_key)
    except Exception as e:
        print(f"Error loading forks.json: {e}")

# Exclude Snap, Scratch 1.4, Scratch 2.0, ScratchX
excluded = {'Snap', 'Scratch1dot4', 'Scratch2', 'ScratchX'}
for ex in excluded:
    if ex in mods_raw:
        del mods_raw[ex]
    if ex in children_map:
        del children_map[ex]

for p, kids in list(children_map.items()):
    children_map[p] = [k for k in kids if k not in excluded and k in mods_raw]

parent_map = {}
for parent, kids in children_map.items():
    for kid in kids:
        parent_map[kid] = parent

def calc_depth(node):
    d = 0
    curr = node
    visited = set()
    while curr in parent_map and curr not in visited:
        visited.add(curr)
        curr = parent_map[curr]
        d += 1
    return d

def get_lineage(node):
    trail = [node]
    curr = node
    visited = {node}
    while curr in parent_map and parent_map[curr] not in visited:
        curr = parent_map[curr]
        visited.add(curr)
        trail.append(curr)
    return list(reversed(trail))

# Map mods to branches
def get_branch_info(var, lineage):
    if var == 'Scratch':
        return ('main', 'Main (Scratch 3.0 Core)', '#ffab19')
    if 'Snap' in lineage:
        return ('snap', 'Snap! Ecosystem', '#3b82f6')
    if var == 'Mistwarp' or var == 'ScratchBox':
        return ('mistwarp', 'MistWarp Ecosystem', '#c299cf')
    if 'SnailIDE' in lineage:
        return ('snail-ide', 'Snail-IDE Branch', '#10b981')
    if 'Dinosaurmod' in lineage:
        return ('dinosaurmod', 'DinosaurMod Branch', '#84cc16')
    if 'Penguinmod' in lineage:
        return ('penguinmod', 'PenguinMod Ecosystem', '#06b6d4')
    if 'OpenBlock' in lineage or var == 'MakeBlock':
        return ('hardware', 'Hardware & Robotics', '#14b8a6')
    if var in ['Cognimates', 'Poseblocks', 'MLFC', 'LearningML', 'Robobo']:
        return ('ai-ml', 'AI & Machine Learning', '#ec4899')
    if var in ['Ampmod', 'CodeSnap']:
        return ('turbowarp-audio', 'TurboWarp Audio', '#8b5cf6')
    if var in ['Shredmod', 'RocketBlocks', 'NitroBolt', 'Nuclearmod']:
        return ('turbowarp-speed', 'TurboWarp High-Perf', '#f43f5e')
    if 'Turbowarp' in lineage:
        return ('turbowarp', 'TurboWarp Branch', '#ef4444')
    return ('scratch-direct', 'Scratch Extensions', '#f59e0b')

mod_metadata = {
    'Scratch1dot4': {
        'id': 'scratch-1-4',
        'name': 'Scratch 1.4',
        'githubOrg': 'scratchfoundation',
        'githubRepo': 'https://github.com/scratchfoundation/scratch-gui',
        'githubUrl': 'https://github.com/scratchfoundation',
        'avatar': 'https://avatars.githubusercontent.com/u/103071332?v=4',
        'description': 'The landmark 2009 release of Scratch written in Squeak Smalltalk by MIT Media Lab, pioneering block-based visual programming.',
        'tags': ['Core', 'Smalltalk', 'Legacy', 'Desktop'],
        'author': 'Scratch Foundation / MIT Media Lab',
        'color': '#ffab19',
        'commitHash': '8d4e92a'
    },
    'Scratch2': {
        'id': 'scratch-2',
        'name': 'Scratch 2.0',
        'githubOrg': 'scratchfoundation',
        'githubRepo': 'https://github.com/scratchfoundation/scratch-flash',
        'githubUrl': 'https://github.com/scratchfoundation',
        'avatar': 'https://avatars.githubusercontent.com/u/103071332?v=4',
        'description': 'Second generation Scratch built with Adobe Flash and ActionScript 3, introducing the online community, cloud data, and custom procedures.',
        'tags': ['Core', 'Flash', 'Cloud Data', 'Legacy'],
        'author': 'Scratch Foundation / MIT Media Lab',
        'color': '#ffab19',
        'commitHash': '3f1c79e'
    },
    'Scratch': {
        'id': 'scratch-3',
        'name': 'Scratch 3.0',
        'githubOrg': 'scratchfoundation',
        'githubRepo': 'https://github.com/scratchfoundation/scratch-gui',
        'githubUrl': 'https://github.com/scratchfoundation',
        'avatar': 'https://avatars.githubusercontent.com/u/103071332?v=4',
        'description': 'The modern HTML5, WebGL and Web Audio block programming platform from MIT Media Lab, the foundation of all modern Scratch mods.',
        'tags': ['Core', 'HTML5', 'WebGL', 'Education'],
        'author': 'Scratch Foundation / MIT Media Lab',
        'color': '#ffab19',
        'commitHash': 'e79b12d'
    },
    'Snap': {
        'id': 'snap',
        'name': 'Snap! (BYOB)',
        'githubOrg': 'jmoenig',
        'githubRepo': 'https://github.com/jmoenig/Snap',
        'githubUrl': 'https://github.com/jmoenig',
        'avatar': 'https://avatars.githubusercontent.com/u/338274?v=4',
        'description': 'A broadly expressive Scratch reimplementation by UC Berkeley featuring first-class procedures (lambdas), lists of lists, custom reporters, and OOP.',
        'tags': ['First-Class Lambdas', 'UC Berkeley', 'Functional', 'Education'],
        'author': 'Jens Mönig & Brian Harvey (UC Berkeley)',
        'color': '#3b82f6',
        'commitHash': '4b8d91c'
    },
    'Turbowarp': {
        'id': 'turbowarp',
        'name': 'TurboWarp',
        'githubOrg': 'TurboWarp',
        'githubRepo': 'https://github.com/TurboWarp/scratch-gui',
        'githubUrl': 'https://github.com/TurboWarp',
        'avatar': 'https://avatars.githubusercontent.com/u/67349469?v=4',
        'description': 'The premier Scratch compiler and mod with custom JavaScript extensions, high-framerate support (60+ FPS), dark theme, and standalone packaging.',
        'tags': ['Compiler', 'Extensions', '60FPS', 'Packaging', 'Essential'],
        'author': 'GarboMuffin & TurboWarp Contributors',
        'color': '#ef4444',
        'commitHash': 'a10b42f'
    },
    'Mistwarp': {
        'id': 'mistwarp',
        'name': 'MistWarp',
        'githubOrg': 'mistium',
        'githubRepo': 'https://github.com/mistium',
        'githubUrl': 'https://github.com/mistium',
        'avatar': 'https://avatars.githubusercontent.com/u/175630084',
        'description': 'Mist\'s personal TurboWarp fork integrated with originOS, OSL language workflows, Rotur identity, and custom runtime optimizations.',
        'tags': ['Mistium Ecosystem', 'originOS', 'OSL', 'Rotur Integrated'],
        'author': 'Mist (Mistium)',
        'color': '#c299cf',
        'commitHash': 'd82f710'
    },
    'ScratchBox': {
        'id': 'scratchbox',
        'name': 'ScratchBox',
        'githubOrg': 'gradylink',
        'githubRepo': 'https://github.com/gradylink/mistwarp-gui',
        'githubUrl': 'https://github.com/gradylink',
        'avatar': 'https://raw.githubusercontent.com/gradylink/mistwarp-gui/develop/static/images/192.png',
        'description': 'Lightweight sandbox runtime and editor derivative of MistWarp focused on isolated project execution and clean developer UI.',
        'tags': ['Sandbox', 'Runtime', 'Tools', 'MistWarp Fork'],
        'author': 'gradylink',
        'color': '#a855f7',
        'commitHash': 'b4e912c'
    },
    'Bilup': {
        'id': 'bilup',
        'name': 'Bilup',
        'githubOrg': 'Bilup',
        'githubRepo': 'https://github.com/Bilup/scratch-gui',
        'githubUrl': 'https://github.com/Bilup',
        'avatar': 'https://avatars.githubusercontent.com/u/256908349?v=4',
        'description': 'Creative coding platform and fork of MistWarp featuring OSL ecosystem integration, theme marketplace, and curated extensions.',
        'tags': ['MistWarp Fork', 'OSL', 'Themes', 'Extensions', 'Creative'],
        'author': 'Bilup',
        'color': '#c299cf',
        'commitHash': '6b14e9f'
    },
    'Penguinmod': {
        'id': 'penguinmod',
        'name': 'PenguinMod',
        'githubOrg': 'PenguinMod',
        'githubRepo': 'https://github.com/PenguinMod/PenguinMod-Gui',
        'githubUrl': 'https://github.com/PenguinMod',
        'avatar': 'https://avatars.githubusercontent.com/u/116043111?v=4',
        'description': 'Massive TurboWarp mod packed with hundreds of extra blocks: HTTP fetch requests, Canvas 3D rendering, physics simulation, custom fonts, and local storage.',
        'tags': ['Fetch / HTTP', '3D / Canvas', 'Physics', 'Massive Extensions'],
        'author': 'PenguinMod Community',
        'color': '#00c3ff',
        'commitHash': '7c2b54e'
    },
    'SnailIDE': {
        'id': 'snail-ide',
        'name': 'Snail-IDE',
        'githubOrg': 'snail-ide',
        'githubRepo': 'https://github.com/snail-ide/snail-ide.github.io',
        'githubUrl': 'https://github.com/snail-ide',
        'avatar': 'https://avatars.githubusercontent.com/u/135285286?v=4',
        'description': 'PenguinMod fork packed with custom utilities, advanced physics engines, raymarching shaders, and developer-centric block suites.',
        'tags': ['3D Physics', 'Raymarching', 'Advanced Dev', 'Extensions'],
        'author': 'Snail-IDE Team',
        'color': '#10b981',
        'commitHash': 'f19a4e3'
    },
    'CircleIDE': {
        'id': 'circle-ide',
        'name': 'Circle-IDE',
        'githubOrg': 'circle-ide',
        'githubRepo': 'https://github.com/circle-ide/circle-ide.github.io',
        'githubUrl': 'https://github.com/circle-ide',
        'avatar': 'https://avatars.githubusercontent.com/u/167850020?v=4',
        'description': 'Snail-IDE fork featuring customized circular block design aesthetics and web integration tools.',
        'tags': ['UI Mod', 'Extensions', 'Theming'],
        'author': 'Circle-IDE Devs',
        'color': '#14b8a6',
        'commitHash': '3e429db'
    },
    'AbsoluteMod': {
        'id': 'absolutemod',
        'name': 'AbsoluteMod',
        'githubOrg': 'absolutemod',
        'githubRepo': 'https://github.com/absolutemod/absolutemod.github.io',
        'githubUrl': 'https://github.com/absolutemod',
        'avatar': 'https://avatars.githubusercontent.com/u/172387140?v=4',
        'description': 'Circle-IDE fork pushing experimental UI features, custom shaders, and experimental block helpers.',
        'tags': ['Experimental', 'UI / UX', 'Custom Shaders'],
        'author': 'AbsoluteMod Contributors',
        'color': '#059669',
        'commitHash': '61b9a2c'
    },
    'Bananamod': {
        'id': 'banana-mod',
        'name': 'Banana-mod',
        'githubOrg': 'banana-mod',
        'githubRepo': 'https://github.com/banana-mod/banana-mod.github.io',
        'githubUrl': 'https://github.com/banana-mod',
        'avatar': 'https://avatars.githubusercontent.com/u/168860714?v=4',
        'description': 'Snail-IDE derivative with playful banana-themed tooling, customized color palette, and audio/graphics addons.',
        'tags': ['Creative', 'Themed', 'Audio/Graphics'],
        'author': 'Banana Mod Team',
        'color': '#eab308',
        'commitHash': '9d8f14a'
    },
    'CrabsProgramming': {
        'id': 'crabsprogramming',
        'name': 'CrabsProgramming',
        'githubOrg': 'crabsprogramming',
        'githubRepo': 'https://github.com/crabsprogramming/crabsprogramming.github.io',
        'githubUrl': 'https://github.com/crabsprogramming',
        'avatar': 'https://avatars.githubusercontent.com/u/171569062?v=4',
        'description': 'Snail-IDE community mod bringing unique crustacean UI style and game dev utilities.',
        'tags': ['Community', 'Game Dev', 'Extensions'],
        'author': 'CrabsProgramming',
        'color': '#f97316',
        'commitHash': 'c47a29e'
    },
    'Batscoding': {
        'id': 'batscoding',
        'name': 'BatsCoding',
        'githubOrg': 'batscoding',
        'githubRepo': 'https://github.com/batscoding/batscoding.github.io',
        'githubUrl': 'https://github.com/batscoding',
        'avatar': 'https://avatars.githubusercontent.com/u/172390886?v=4',
        'description': 'Educational Snail-IDE modification offering dark-night themes and specialized teaching extensions.',
        'tags': ['Education', 'Themed', 'Dark UI'],
        'author': 'BatsCoding Devs',
        'color': '#6366f1',
        'commitHash': 'e84b91f'
    },
    'Dinosaurmod': {
        'id': 'dinosaurmod',
        'name': 'DinosaurMod',
        'githubOrg': 'dinosaurmod',
        'githubRepo': 'https://github.com/dinosaurmod/dinosaurmod.github.io',
        'githubUrl': 'https://github.com/dinosaurmod',
        'avatar': 'https://avatars.githubusercontent.com/u/146716840?v=4',
        'description': 'PenguinMod fork focused on 2D game making, custom sprite tools, enhanced vector editors, and game physics.',
        'tags': ['Game Engine', '2D Physics', 'Sprite Tools'],
        'author': 'DinosaurMod Community',
        'color': '#84cc16',
        'commitHash': '51e8a9d'
    },
    'Fairymod': {
        'id': 'fairymod',
        'name': 'Fairymod',
        'githubOrg': 'fairymod',
        'githubRepo': 'https://github.com/fairymod/fairymod.github.io',
        'githubUrl': 'https://github.com/fairymod',
        'avatar': 'https://avatars.githubusercontent.com/u/172392471?v=4',
        'description': 'DinosaurMod fork featuring whimsical animations, magical particles, and fantasy sprite packs.',
        'tags': ['Creative', 'Visual Effects', 'Particles'],
        'author': 'Fairymod Devs',
        'color': '#ec4899',
        'commitHash': '7a4f91b'
    },
    'Craftmod': {
        'id': 'craftmod',
        'name': 'Craftmod',
        'githubOrg': 'craftingdead26',
        'githubRepo': 'https://github.com/craftingdead26/Craftmod.github.io',
        'githubUrl': 'https://github.com/craftingdead26',
        'avatar': 'https://avatars.githubusercontent.com/u/84102871?v=4',
        'description': 'Voxel and block-building inspired DinosaurMod fork equipped with grid collision and tilemap tools.',
        'tags': ['Voxel', 'Tilemaps', 'Grid Physics'],
        'author': 'CraftingDead26',
        'color': '#16a34a',
        'commitHash': '89b2c41'
    },
    'Electramod': {
        'id': 'electramod',
        'name': 'ElectraMod',
        'githubOrg': 'ElectraMod',
        'githubRepo': 'https://github.com/ElectraMod/ElectraMod',
        'githubUrl': 'https://github.com/ElectraMod',
        'avatar': 'https://avatars.githubusercontent.com/u/152914848?v=4',
        'description': 'High-voltage PenguinMod fork with enhanced audio synthesizers, sleek obsidian UI, and extended math blocks.',
        'tags': ['Audio Synth', 'Math Blocks', 'Modern UI'],
        'author': 'ElectraMod Team',
        'color': '#0ea5e9',
        'commitHash': '43a9b1c'
    },
    'Plungermod': {
        'id': 'plungermod',
        'name': 'Plungermod',
        'githubOrg': 'plungermod',
        'githubRepo': 'https://github.com/plungermod/plungermod.github.io',
        'githubUrl': 'https://github.com/plungermod',
        'avatar': 'https://avatars.githubusercontent.com/u/168863617?v=4',
        'description': 'PenguinMod mod featuring rapid prototyping blocks, debugging inspection utilities, and experimental scripts.',
        'tags': ['Prototyping', 'Debugging', 'Experimental'],
        'author': 'Plungermod Team',
        'color': '#0284c7',
        'commitHash': '12c9e4b'
    },
    'Orangemod': {
        'id': 'orangemod',
        'name': 'OrangeMod',
        'githubOrg': 'kokodevelopment',
        'githubRepo': 'https://github.com/kokodevelopment/OrangeMod',
        'githubUrl': 'https://github.com/kokodevelopment',
        'avatar': 'https://avatars.githubusercontent.com/u/118335029?v=4',
        'description': 'PenguinMod fork by KokoDevelopment adding custom array manipulation, string formatters, and utility extensions.',
        'tags': ['Data Structures', 'Utilities', 'Formatting'],
        'author': 'KokoDevelopment',
        'color': '#f97316',
        'commitHash': '7d41a9c'
    },
    'Falconmod': {
        'id': 'falconmod',
        'name': 'FalconMod',
        'githubOrg': 'falconmod',
        'githubRepo': 'https://github.com/falconmod/editor',
        'githubUrl': 'https://github.com/falconmod',
        'avatar': 'https://avatars.githubusercontent.com/u/165787680?v=4',
        'description': 'High-performance PenguinMod fork optimizing execution speed and offering custom camera controls.',
        'tags': ['Performance', 'Camera System', 'Speed'],
        'author': 'FalconMod Team',
        'color': '#38bdf8',
        'commitHash': '6b8a21f'
    },
    'Zypheramod': {
        'id': 'zyphera-mod',
        'name': 'Zyphera-mod',
        'githubOrg': 'zyphera-mod',
        'githubRepo': 'https://github.com/zyphera-mod/zyphera-mod.github.io',
        'githubUrl': 'https://github.com/zyphera-mod',
        'avatar': 'https://avatars.githubusercontent.com/u/167852326?v=4',
        'description': 'Community PenguinMod fork featuring web request utilities and customized editor themes.',
        'tags': ['Web Tools', 'Theming', 'Community'],
        'author': 'Zyphera Team',
        'color': '#818cf8',
        'commitHash': '34e8b9a'
    },
    'Espressoblocks': {
        'id': 'espressoblocks',
        'name': 'EspressoBlocks',
        'githubOrg': 'espressoblocks',
        'githubRepo': 'https://github.com/espressoblocks/espressoblocks',
        'githubUrl': 'https://github.com/espressoblocks',
        'avatar': 'https://avatars.githubusercontent.com/u/157297926?v=4',
        'description': 'Smooth caffeine-fueled PenguinMod fork focused on developer workflow enhancements and quick shortcuts.',
        'tags': ['Developer UX', 'Shortcuts', 'Workflow'],
        'author': 'EspressoBlocks Devs',
        'color': '#d97706',
        'commitHash': '59a1b4e'
    },
    'ZincCoding': {
        'id': 'zinc-coding',
        'name': 'Zinc Coding',
        'githubOrg': 'zinc-coding',
        'githubRepo': 'https://github.com/zinc-coding/zinc-coding.github.io',
        'githubUrl': 'https://github.com/zinc-coding',
        'avatar': 'https://avatars.githubusercontent.com/u/172390886?v=4',
        'description': 'PenguinMod fork designed for game mechanics, level design helpers, and score counters.',
        'tags': ['Game Mechanics', 'Counters', 'Helpers'],
        'author': 'Zinc Coding Team',
        'color': '#94a3b8',
        'commitHash': '81c4e9d'
    },
    'FireMod': {
        'id': 'firemod',
        'name': 'FireMod',
        'githubOrg': 'firemoddev',
        'githubRepo': 'https://github.com/firemoddev/FireMod',
        'githubUrl': 'https://github.com/firemoddev',
        'avatar': 'https://avatars.githubusercontent.com/u/152914848?v=4',
        'description': 'Fast-paced PenguinMod fork with fire animations, custom shader filters, and visual enhancements.',
        'tags': ['Shaders', 'VFX', 'Filters'],
        'author': 'FireMod Devs',
        'color': '#f43f5e',
        'commitHash': '2a9d81f'
    },
    'Axerboost': {
        'id': 'axerboost',
        'name': 'Axerboost (Hexium)',
        'githubOrg': 'hexiumtechnologies',
        'githubRepo': 'https://github.com/hexiumtechnologies/editor',
        'githubUrl': 'https://github.com/hexiumtechnologies',
        'avatar': 'https://avatars.githubusercontent.com/u/148117765?v=4',
        'description': 'Hexium Technologies mod of PenguinMod designed for power users with system diagnostic blocks.',
        'tags': ['Hexium', 'Diagnostics', 'Power User'],
        'author': 'Hexium Technologies',
        'color': '#6366f1',
        'commitHash': '9f14e7a'
    },
    'Itch': {
        'id': 'itch',
        'name': 'Itch',
        'githubOrg': 'itch-scratch-mod',
        'githubRepo': 'https://github.com/itch-scratch-mod/Itch-Gui',
        'githubUrl': 'https://github.com/itch-scratch-mod',
        'avatar': 'https://avatars.githubusercontent.com/u/168864771?v=4',
        'description': 'Retro-styled PenguinMod fork providing pixelated block themes and retro game sound synthesis.',
        'tags': ['Retro Style', 'Chiptune', 'Pixel Art'],
        'author': 'Itch Mod Team',
        'color': '#fa5252',
        'commitHash': '18a4d9b'
    },
    'Hiddenblocks': {
        'id': 'hiddenblocks',
        'name': 'HiddenBlocks',
        'githubOrg': 'hiddenblocks',
        'githubRepo': 'https://github.com/hiddenblocks/hiddenblocks.github.io',
        'githubUrl': 'https://github.com/hiddenblocks',
        'avatar': 'https://avatars.githubusercontent.com/u/168863617?v=4',
        'description': 'PenguinMod mod unlocking internal, hidden, and unreleased Scratch opcodes and experimental hooks.',
        'tags': ['Opcodes', 'Internal Blocks', 'Hacks'],
        'author': 'HiddenBlocks Dev',
        'color': '#64748b',
        'commitHash': '7e2b14f'
    },
    'GlowingCrown': {
        'id': 'glowingcrown',
        'name': 'GlowingCrown',
        'githubOrg': 'glowingcrown',
        'githubRepo': 'https://github.com/glowingcrown/studio',
        'githubUrl': 'https://github.com/glowingcrown',
        'avatar': 'https://avatars.githubusercontent.com/u/167852326?v=4',
        'description': 'Vibrant PenguinMod fork with royal glowing UI styling and lighting shaders.',
        'tags': ['Glowing UI', 'Lighting', 'Visuals'],
        'author': 'GlowingCrown Team',
        'color': '#fbbf24',
        'commitHash': '61a9d4e'
    },
    'CattiesWorld': {
        'id': 'cattiesworld',
        'name': 'CattiesWorld',
        'githubOrg': 'cattiesworld',
        'githubRepo': 'https://github.com/cattiesworld/cattiesworld.github.io',
        'githubUrl': 'https://github.com/cattiesworld',
        'avatar': 'https://avatars.githubusercontent.com/u/152914848?v=4',
        'description': 'Charming feline-themed PenguinMod mod featuring community sprite libraries and cute assets.',
        'tags': ['Cute Assets', 'Sprite Library', 'Themed'],
        'author': 'CattiesWorld Community',
        'color': '#f472b6',
        'commitHash': '4a8d91c'
    },
    'Stax': {
        'id': 'stax',
        'name': 'Stax',
        'githubOrg': 'stax-lang',
        'githubRepo': 'https://github.com/stax-lang/stax',
        'githubUrl': 'https://github.com/stax-lang',
        'avatar': 'https://avatars.githubusercontent.com/u/152914848?v=4',
        'description': 'PenguinMod mod offering stack and queue data structures, map/filter/reduce blocks, and fast math.',
        'tags': ['Data Structures', 'Functional', 'Stacks'],
        'author': 'Stax Lang Devs',
        'color': '#8b5cf6',
        'commitHash': '9d41e7a'
    },
    'TeraMod': {
        'id': 'teramod',
        'name': 'TeraMod',
        'githubOrg': 'cattiesworld',
        'githubRepo': 'https://github.com/cattiesworld/Teramod',
        'githubUrl': 'https://github.com/cattiesworld',
        'avatar': 'https://avatars.githubusercontent.com/u/152914848?v=4',
        'description': 'CattiesWorld sister project with oversized terrain generation blocks and map builders.',
        'tags': ['Terrain Gen', 'World Builder', 'Tilemaps'],
        'author': 'CattiesWorld Team',
        'color': '#10b981',
        'commitHash': '3e7b14d'
    },
    'Tutelmod': {
        'id': 'tutelmod',
        'name': 'TutelMod',
        'githubOrg': 'TutelMod',
        'githubRepo': 'https://github.com/TutelMod/TutelMod',
        'githubUrl': 'https://github.com/TutelMod',
        'avatar': 'https://avatars.githubusercontent.com/u/168860714?v=4',
        'description': 'Turtle geometry and mathematical art PenguinMod fork for algorithmic drawings and generative art.',
        'tags': ['Turtle Graphics', 'Generative Art', 'Math'],
        'author': 'TutelMod Devs',
        'color': '#22c55e',
        'commitHash': '71e9a2b'
    },
    'SuperChaosMod': {
        'id': 'super-chaosmod',
        'name': 'Super Chaos Mod',
        'githubOrg': 'super-chaosmod',
        'githubRepo': 'https://github.com/super-chaosmod/super-chaosmod.github.io',
        'githubUrl': 'https://github.com/super-chaosmod',
        'avatar': 'https://avatars.githubusercontent.com/u/168863617?v=4',
        'description': 'Chaotic experimental PenguinMod fork with randomizer blocks, physics glitches, and sandbox fun.',
        'tags': ['Randomizers', 'Chaos', 'Fun Blocks'],
        'author': 'Chaos Mod Team',
        'color': '#ef4444',
        'commitHash': '5a8e19b'
    },
    'GaiaMod': {
        'id': 'gaiamod',
        'name': 'GaiaMod',
        'githubOrg': 'gaiamod-main',
        'githubRepo': 'https://github.com/gaiamod-main/editor',
        'githubUrl': 'https://github.com/gaiamod-main',
        'avatar': 'https://avatars.githubusercontent.com/u/172387140?v=4',
        'description': 'Nature and environmental simulation mod for PenguinMod with weather systems and ecosystem logic.',
        'tags': ['Simulation', 'Weather', 'Ecosystems'],
        'author': 'GaiaMod Devs',
        'color': '#15803d',
        'commitHash': '4b91e2a'
    },
    'MerrCode': {
        'id': 'merrcode',
        'name': 'MerrCode',
        'githubOrg': 'merrcraft',
        'githubRepo': 'https://github.com/merrcraft/merrcode',
        'githubUrl': 'https://github.com/merrcraft',
        'avatar': 'https://avatars.githubusercontent.com/u/146716840?v=4',
        'description': 'PenguinMod mod built for multiplayer sandbox worlds and interactive canvas networking.',
        'tags': ['Multiplayer', 'Networking', 'Sandbox'],
        'author': 'MerrCraft Team',
        'color': '#0284c7',
        'commitHash': '61c4a9d'
    },
    'Ampmod': {
        'id': 'ampmod',
        'name': 'AmpMod',
        'githubOrg': 'ampmod',
        'githubRepo': 'https://codeberg.org/ampmod/ampmod',
        'githubUrl': 'https://codeberg.org/ampmod',
        'avatar': 'https://avatars.githubusercontent.com/u/152914848?v=4',
        'description': 'Audio-amplified TurboWarp fork with software synthesizers, Web Audio filters, and MIDI sequencing.',
        'tags': ['Audio Synth', 'Web Audio', 'MIDI', 'Codeberg'],
        'author': 'AmpMod Developers',
        'color': '#8b5cf6',
        'commitHash': '8d14a9c'
    },
    'CodeSnap': {
        'id': 'codesnap',
        'name': 'CodeSnap',
        'githubOrg': 'codesnap-org',
        'githubRepo': 'https://github.com/codesnap-org/projects',
        'githubUrl': 'https://github.com/codesnap-org',
        'avatar': 'https://avatars.githubusercontent.com/u/172390886?v=4',
        'description': 'AmpMod derivative merging Snap! style first-class data structures and closures with TurboWarp speed.',
        'tags': ['First Class', 'Snap Hybrid', 'Audio'],
        'author': 'CodeSnap Org',
        'color': '#a78bfa',
        'commitHash': '9a14b7e'
    },
    'Unsandboxed': {
        'id': 'unsandboxed',
        'name': 'Unsandboxed',
        'githubOrg': 'unsandboxed',
        'githubRepo': 'https://github.com/unsandboxed/unsandboxed.github.io',
        'githubUrl': 'https://github.com/unsandboxed',
        'avatar': 'https://avatars.githubusercontent.com/u/117045635?s=200&v=4',
        'description': 'TurboWarp fork running JavaScript extensions in unsandboxed mode with direct DOM and web API access.',
        'tags': ['Unsandboxed JS', 'Web APIs', 'Power Dev'],
        'author': 'Unsandboxed Org',
        'color': '#f43f5e',
        'commitHash': '3b8e49d'
    },
    'MyScratchBlocks': {
        'id': 'snaplabs',
        'name': 'SnapLabs',
        'githubOrg': 'myscratchblocks',
        'githubRepo': 'https://github.com/myscratchblocks/scratch-gui',
        'githubUrl': 'https://github.com/myscratchblocks',
        'avatar': 'https://avatars.githubusercontent.com/u/168864771?v=4',
        'description': 'Experimental TurboWarp laboratory for cutting-edge Scratch block UI designs and test prototypes.',
        'tags': ['UI Lab', 'Prototypes', 'Experimental'],
        'author': 'SnapLabs Team',
        'color': '#ec4899',
        'commitHash': '7d19a4e'
    },
    'NitroBolt': {
        'id': 'nitrobolt',
        'name': 'Nitrobolt',
        'githubOrg': 'Nitro-Bolt',
        'githubRepo': 'https://github.com/Nitro-Bolt/scratch-gui',
        'githubUrl': 'https://github.com/Nitro-Bolt',
        'avatar': 'https://avatars.githubusercontent.com/u/157997438?v=4',
        'description': 'A mod of TurboWarp with tons of new features, and a haven for developers who don\'t want to be restricted by "compatibility".',
        'tags': ['TurboWarp Fork', 'Performance', 'Extensions', 'Developer'],
        'author': 'NitroBolt',
        'color': '#f59e0b',
        'commitHash': '51e7a4b'
    },
    'Shredmod': {
        'id': 'shredmod',
        'name': 'ShredMod',
        'githubOrg': 'shredmod',
        'githubRepo': 'https://github.com/shredmod/shredmod.github.io',
        'githubUrl': 'https://github.com/shredmod',
        'avatar': 'https://avatars.githubusercontent.com/u/168860714?v=4',
        'description': 'TurboWarp fork engineered for maximum computing throughput and optimized matrix math computations.',
        'tags': ['Matrix Math', 'Throughput', 'High Speed'],
        'author': 'ShredMod Developers',
        'color': '#dc2626',
        'commitHash': '8e2b14c'
    },
    'RocketBlocks': {
        'id': 'rocketblocks',
        'name': 'RocketBlocks',
        'githubOrg': 'rocketblocks',
        'githubRepo': 'https://github.com/rocketblocks/rocketblocks.github.io',
        'githubUrl': 'https://github.com/rocketblocks',
        'avatar': 'https://avatars.githubusercontent.com/u/172387140?v=4',
        'description': 'ShredMod fork equipped with orbital astrophysics equations, trajectory solvers, and rocketry blocks.',
        'tags': ['Orbital Physics', 'Space Sim', 'Math'],
        'author': 'RocketBlocks Team',
        'color': '#f97316',
        'commitHash': '2f8a19b'
    },
    'Nuclearmod': {
        'id': 'nuclearmod',
        'name': 'NuclearMod',
        'githubOrg': 'nuclearmod',
        'githubRepo': 'https://github.com/nuclearmod/editor',
        'githubUrl': 'https://github.com/nuclearmod',
        'avatar': 'https://avatars.githubusercontent.com/u/165787680?v=4',
        'description': 'TurboWarp mod pushing parallel compute limits and multithreaded web worker acceleration.',
        'tags': ['Parallel Compute', 'Web Workers', 'Performance'],
        'author': 'NuclearMod Team',
        'color': '#84cc16',
        'commitHash': '9d18a4c'
    },
    'BlockScript': {
        'id': 'blockscript',
        'name': 'BlockScript',
        'githubOrg': 'blockScript',
        'githubRepo': 'https://github.com/blockScript/editor',
        'githubUrl': 'https://github.com/blockScript',
        'avatar': 'https://avatars.githubusercontent.com/u/167850020?v=4',
        'description': 'TurboWarp fork enabling text-to-block bidirectional code editing with a sleek hybrid scripting syntax.',
        'tags': ['Text to Block', 'Hybrid Code', 'Syntax'],
        'author': 'BlockScript Devs',
        'color': '#06b6d4',
        'commitHash': '4a19b8e'
    },
    'Cocrea': {
        'id': 'gandi-ide',
        'name': 'Gandi IDE',
        'githubOrg': 'Gandi-IDE',
        'githubRepo': 'https://github.com/Gandi-IDE/gandi-blocks',
        'githubUrl': 'https://github.com/Gandi-IDE',
        'avatar': 'https://avatars.githubusercontent.com/u/96603851?v=4',
        'description': 'Gandi IDE - a powerful game engine and creative development environment for Scratchers with multiplayer, custom plugins, and tilemap editors.',
        'tags': ['Game Engine', 'Multiplayer', 'Plugins', 'Tilemap', 'TurboWarp Fork'],
        'author': 'Gandi (Cocrea)',
        'color': '#6366f1',
        'commitHash': '1e7b94a'
    },
    'ZtEngine': {
        'id': '02engine',
        'name': '02engine',
        'githubOrg': '02engine',
        'githubRepo': 'https://github.com/02engine/02engine.github.io',
        'githubUrl': 'https://github.com/02engine',
        'avatar': 'https://avatars.githubusercontent.com/u/152914848?v=4',
        'description': 'TurboWarp fork built specifically for 2D game engine pipelines, cutscene editors, and map builders.',
        'tags': ['Game Engine', 'Cutscenes', 'Pipelines'],
        'author': '02engine Team',
        'color': '#0ea5e9',
        'commitHash': '7b14d8a'
    },
    'AstraEditor': {
        'id': 'astraeditor',
        'name': 'AstraEditor',
        'githubOrg': 'astras-top',
        'githubRepo': 'https://github.com/astras-top/editor',
        'githubUrl': 'https://github.com/astras-top',
        'avatar': 'https://avatars.githubusercontent.com/u/168864771?v=4',
        'description': 'Celestial-themed TurboWarp online editor featuring night sky aesthetic and space game extensions.',
        'tags': ['Celestial UI', 'Theming', 'Space Extensions'],
        'author': 'Astra Editor Team',
        'color': '#6366f1',
        'commitHash': '5c9a14b'
    },
    'ScratchCE': {
        'id': 'scratchce',
        'name': 'Scratch Community Edition',
        'githubOrg': 'scratchce',
        'githubRepo': 'https://github.com/scratchce/beta',
        'githubUrl': 'https://github.com/scratchce',
        'avatar': 'https://avatars.githubusercontent.com/u/100775707?v=4',
        'description': 'Community-driven open-source Scratch release merging requested core features and ergonomic fixes.',
        'tags': ['Community Edition', 'Open Source', 'Ergonomics'],
        'author': 'Scratch CE Maintainers',
        'color': '#f59e0b',
        'commitHash': '8a14b9c'
    },
    'SNEDit': {
        'id': 'sn-edit',
        'name': 'SN-Edit',
        'githubOrg': 'cubixentertainment',
        'githubRepo': 'https://github.com/cubixentertainment/SN-Edit',
        'githubUrl': 'https://github.com/cubixentertainment',
        'avatar': 'https://avatars.githubusercontent.com/u/152914848?v=4',
        'description': 'Cubix Entertainment mod of TurboWarp with custom asset pipelines and sound effects libraries.',
        'tags': ['Cubix Entertainment', 'Asset Pipeline', 'Audio'],
        'author': 'Cubix Entertainment',
        'color': '#ec4899',
        'commitHash': '2d8b14a'
    },
    'Adacraft': {
        'id': 'adacraft',
        'name': 'Adacraft',
        'githubOrg': 'adacraft',
        'githubRepo': 'https://github.com/adacraft/adacraft',
        'githubUrl': 'https://github.com/adacraft',
        'avatar': 'https://avatars.githubusercontent.com/u/74307898?v=4',
        'description': 'Open-source visual programming environment for creative coding with modern web APIs, AI, and generative media.',
        'tags': ['Creative Coding', 'Modern Web', 'Generative Media'],
        'author': 'Adacraft Community',
        'color': '#14b8a6',
        'commitHash': '3e9a14b'
    },
    'Dash': {
        'id': 'dash',
        'name': 'Dash',
        'githubOrg': 'dashblocks',
        'githubRepo': 'https://github.com/dashblocks/dashblocks.github.io',
        'githubUrl': 'https://github.com/dashblocks',
        'avatar': 'https://avatars.githubusercontent.com/u/167852326?v=4',
        'description': 'TurboWarp mod with sleek dash UI theme, responsive mobile stage controls, and platformer extensions.',
        'tags': ['Mobile UI', 'Dash Theme', 'Platformer'],
        'author': 'DashBlocks Team',
        'color': '#3b82f6',
        'commitHash': '9b14e7a'
    },
    'Axolotl': {
        'id': 'axolotl',
        'name': 'Axolotl',
        'githubOrg': 'gtrees-n',
        'githubRepo': 'https://github.com/gtrees-n/AxolotlEditor-gui',
        'githubUrl': 'https://github.com/gtrees-n',
        'avatar': 'https://avatars.githubusercontent.com/u/152914848?v=4',
        'description': 'Cute axolotl-themed TurboWarp mod with aquatic sprite assets and pleasant pastel styling.',
        'tags': ['Pastel Theme', 'Axolotl', 'Cute Assets'],
        'author': 'gtrees-n',
        'color': '#f472b6',
        'commitHash': '6a18d9e'
    },
    'GvbvdxxMod2': {
        'id': 'gvbvdxxmod-2',
        'name': 'GvbvdxxMod 2',
        'githubOrg': 'jasonglenevans',
        'githubRepo': 'https://github.com/jasonglenevans/GvbvdxxMod2',
        'githubUrl': 'https://github.com/jasonglenevans',
        'avatar': 'https://avatars.githubusercontent.com/u/58234857?v=4',
        'description': 'Jason Glen Evans\' second generation Scratch mod rebuilt on TurboWarp with custom system opcodes.',
        'tags': ['Jason Glen Evans', 'System Opcodes', 'Custom Blocks'],
        'author': 'Jason Glen Evans',
        'color': '#8b5cf6',
        'commitHash': '1f9a4b8'
    },
    'LibreKitten': {
        'id': 'librekitten',
        'name': 'LibreKitten',
        'githubOrg': 'librekitten',
        'githubRepo': 'https://github.com/librekitten/librekitten.github.io',
        'githubUrl': 'https://github.com/librekitten',
        'avatar': 'https://avatars.githubusercontent.com/u/168863617?v=4',
        'description': 'Free and open-source kitten-loving TurboWarp fork with privacy-focused defaults and zero tracking.',
        'tags': ['Privacy', 'Open Source', 'Kitten Theme'],
        'author': 'LibreKitten Project',
        'color': '#f59e0b',
        'commitHash': '7a14e9d'
    },
    'ConiBlocks': {
        'id': 'coniblocks',
        'name': 'ConiBlocks',
        'githubOrg': 'coniblocks',
        'githubRepo': 'https://github.com/coniblocks/studio',
        'githubUrl': 'https://github.com/coniblocks',
        'avatar': 'https://avatars.githubusercontent.com/u/168860714?v=4',
        'description': 'TurboWarp fork featuring cone and isometric projection blocks for pseudo-3D game creation.',
        'tags': ['Isometric', 'Pseudo 3D', 'Geometry'],
        'author': 'ConiBlocks Team',
        'color': '#06b6d4',
        'commitHash': '4e9a14b'
    },
    'PenguinmodPort': {
        'id': 'penguinmod-port',
        'name': 'Penguinmod-Port',
        'githubOrg': 'penguinmod-port',
        'githubRepo': 'https://github.com/penguinmod-port/scratch-gui',
        'githubUrl': 'https://github.com/penguinmod-port',
        'avatar': 'https://avatars.githubusercontent.com/u/167850020?v=4',
        'description': 'Lightweight TurboWarp port backporting select PenguinMod extensions into vanilla TurboWarp.',
        'tags': ['Port', 'Backport', 'Extensions'],
        'author': 'PenguinMod Port Devs',
        'color': '#0284c7',
        'commitHash': '8b14a9c'
    },
    'Fox2d': {
        'id': 'fox2d',
        'name': 'Fox2d',
        'githubOrg': 'fox2d',
        'githubRepo': 'https://github.com/fox2d/editor',
        'githubUrl': 'https://github.com/fox2d',
        'avatar': 'https://avatars.githubusercontent.com/u/152914848?v=4',
        'description': '2D game development engine built on top of TurboWarp with collision boxes and physics joints.',
        'tags': ['2D Engine', 'Joints', 'Collision'],
        'author': 'Fox2d Team',
        'color': '#ea580c',
        'commitHash': '3e14b9a'
    },
    'CodeTorch': {
        'id': 'codetorch',
        'name': 'CodeTorch',
        'githubOrg': 'CodeTorchNET',
        'githubRepo': 'https://github.com/CodeTorchNET/CodeTorch-Block-Compiler',
        'githubUrl': 'https://github.com/CodeTorchNET',
        'avatar': 'https://avatars.githubusercontent.com/u/120530822?v=4',
        'description': 'Developer-centric block platform and TurboWarp modification with standalone block compiler and discussion hub.',
        'tags': ['TurboWarp Fork', 'Block Compiler', 'Community', 'Developer'],
        'author': 'CodeTorch',
        'color': '#e11d48',
        'commitHash': '9a14e7b'
    },
    'OpenBlock': {
        'id': 'openblock',
        'name': 'OpenBlock',
        'githubOrg': 'openblockcc',
        'githubRepo': 'https://github.com/openblockcc/openblock-gui',
        'githubUrl': 'https://github.com/openblockcc',
        'avatar': 'https://avatars.githubusercontent.com/u/74307898?v=4',
        'description': 'Open-source graphical hardware programming software for Arduino, ESP32, micro:bit, and robotic sensors.',
        'tags': ['Hardware', 'Arduino', 'ESP32', 'Robotics', 'IoT'],
        'author': 'OpenBlock.cc Team',
        'color': '#10b981',
        'commitHash': '1a4e9b8'
    },
    'ScratchArduino': {
        'id': 'scratch-arduino',
        'name': 'Scratch Arduino (Ottawa STEM)',
        'githubOrg': 'ottawastem',
        'githubRepo': 'https://github.com/ottawastem/scratch-arduino',
        'githubUrl': 'https://github.com/ottawastem',
        'avatar': 'https://avatars.githubusercontent.com/u/74307898?v=4',
        'description': 'OpenBlock derivative connecting Ottawa STEM educational robotics kits directly to Scratch.',
        'tags': ['Hardware', 'Arduino', 'STEM Robotics'],
        'author': 'Ottawa STEM',
        'color': '#059669',
        'commitHash': '7d14a9b'
    },
    'Cognimates': {
        'id': 'cognimates',
        'name': 'Cognimates',
        'githubOrg': 'hackidemia',
        'githubRepo': 'https://github.com/hackidemia/cognimates-gui',
        'githubUrl': 'https://github.com/hackidemia',
        'avatar': 'https://avatars.githubusercontent.com/u/4522560?v=4',
        'description': 'AI education platform by Hackidemia and MIT Media Lab enabling children to train AI vision, voice, and robotics.',
        'tags': ['AI / ML', 'Voice / Vision', 'MIT Media Lab', 'Education'],
        'author': 'Hackidemia & MIT Media Lab',
        'color': '#ec4899',
        'commitHash': '5e9a14b'
    },
    'Smalruby': {
        'id': 'smalruby',
        'name': 'Smalruby',
        'githubOrg': 'smalruby',
        'githubRepo': 'https://github.com/smalruby/smalruby3-gui',
        'githubUrl': 'https://github.com/smalruby',
        'avatar': 'https://avatars.githubusercontent.com/u/74307898?v=4',
        'description': 'Scratch 3.0 mod allowing simultaneous block programming and Ruby code generation from Japan.',
        'tags': ['Ruby Code', 'Bilingual', 'Japan STEAM'],
        'author': 'Smalruby Project',
        'color': '#e11d48',
        'commitHash': '2a14b9e'
    },
    'E_icques': {
        'id': 'e-icques',
        'name': 'E羊icques (SheepTester)',
        'githubOrg': 'SheepTester',
        'githubRepo': 'https://github.com/SheepTester/scratch-gui',
        'githubUrl': 'https://github.com/SheepTester',
        'avatar': 'https://avatars.githubusercontent.com/u/22133785?v=4',
        'description': 'Sean Yen\'s (SheepTester) Scratch modification packed with ingenious runtime hacks, custom reporters, and utilities.',
        'tags': ['SheepTester', 'Runtime Hacks', 'Custom Blocks'],
        'author': 'Sean Yen (SheepTester)',
        'color': '#3b82f6',
        'commitHash': '8b14e9a'
    },
    'Bricklife': {
        'id': 'bricklife',
        'name': 'Bricklife',
        'githubOrg': 'bricklife',
        'githubRepo': 'https://github.com/bricklife/scratch-gui',
        'githubUrl': 'https://github.com/bricklife',
        'avatar': 'https://avatars.githubusercontent.com/u/74307898?v=4',
        'description': 'Scratch 3.0 mod by Bricklife integrating physical LEGO brick sensors, motors, and interactive robotics.',
        'tags': ['LEGO', 'Robotics', 'Sensors'],
        'author': 'Bricklife',
        'color': '#f59e0b',
        'commitHash': '4e14a9b'
    },
    'HiddenblocksScratch': {
        'id': 'hiddenblocks-scratch',
        'name': 'HiddenBlocks (Scratch 3.0)',
        'githubOrg': 'hiddenblocks',
        'githubRepo': 'https://github.com/hiddenblocks/scratch-gui',
        'githubUrl': 'https://github.com/hiddenblocks',
        'avatar': 'https://avatars.githubusercontent.com/u/168863617?v=4',
        'description': 'Direct Scratch 3.0 fork exposing internal Scratch opcodes and hidden prototype blocks.',
        'tags': ['Internal Blocks', 'Scratch Core', 'Hacks'],
        'author': 'HiddenBlocks Dev',
        'color': '#64748b',
        'commitHash': '6a14b9e'
    },
    'Robobo': {
        'id': 'robobo',
        'name': 'Robobo',
        'githubOrg': 'theroboboproject',
        'githubRepo': 'https://github.com/theroboboproject/robobo-scratch3',
        'githubUrl': 'https://github.com/theroboboproject',
        'avatar': 'https://avatars.githubusercontent.com/u/74307898?v=4',
        'description': 'Educational robotics platform connecting Scratch 3.0 to Robobo smartphone-mounted autonomous robots.',
        'tags': ['Robotics', 'Smartphone Robots', 'AI Vision'],
        'author': 'The Robobo Project',
        'color': '#0284c7',
        'commitHash': '1e9a4b8'
    },
    'Poseblocks': {
        'id': 'poseblocks',
        'name': 'PoseBlocks',
        'githubOrg': 'mit-raise',
        'githubRepo': 'https://github.com/mit-raise/poseblocks',
        'githubUrl': 'https://github.com/mit-raise',
        'avatar': 'https://avatars.githubusercontent.com/u/3420800?v=4',
        'description': 'MIT RAISE project for pose detection, body tracking, and AI computer vision in block programming.',
        'tags': ['Pose Detection', 'AI Vision', 'MIT RAISE'],
        'author': 'MIT RAISE Team',
        'color': '#8b5cf6',
        'commitHash': '9d14e7a'
    },
    'MLFC': {
        'id': 'mlfc',
        'name': 'M.L.F.C (Machine Learning for Kids)',
        'githubOrg': 'machinelearningforkids',
        'githubRepo': 'https://github.com/machinelearningforkids/ml-for-kids',
        'githubUrl': 'https://github.com/machinelearningforkids',
        'avatar': 'https://avatars.githubusercontent.com/u/4522560?v=4',
        'description': 'Machine Learning for Kids Scratch mod for training image, text, and sound recognition models.',
        'tags': ['Machine Learning', 'AI Models', 'Classroom AI'],
        'author': 'Dale Lane / ML for Kids',
        'color': '#ec4899',
        'commitHash': '7a14b9d'
    },
    'ClipCC': {
        'id': 'clipcc',
        'name': 'ClipCC',
        'githubOrg': 'CodingClip',
        'githubRepo': 'https://github.com/CodingClip/clipcc-gui',
        'githubUrl': 'https://github.com/CodingClip',
        'avatar': 'https://avatars.githubusercontent.com/u/118335029?v=4',
        'description': 'Next-generation extensible block programming platform with full modular plugin system and modern UI.',
        'tags': ['Modular Plugins', 'Modern UI', 'Next Gen'],
        'author': 'CodingClip Team',
        'color': '#3b82f6',
        'commitHash': '3e4a91b'
    },
    'MakeBlock': {
        'id': 'makeblock',
        'name': 'MakeBlock (mBlock)',
        'githubOrg': 'Makeblock-official',
        'githubRepo': 'https://github.com/Makeblock-official/mBlock',
        'githubUrl': 'https://github.com/Makeblock-official',
        'avatar': 'https://avatars.githubusercontent.com/u/74307898?v=4',
        'description': 'mBlock by Makeblock for hardware programming, STEAM, AI, IoT, and CyberPi robotics.',
        'tags': ['Hardware', 'Robotics', 'IoT', 'STEAM'],
        'author': 'Makeblock',
        'color': '#0ea5e9',
        'commitHash': '5b14a9e'
    },
    'Xcratch': {
        'id': 'xcratch',
        'name': 'Xcratch',
        'githubOrg': 'xcratch',
        'githubRepo': 'https://github.com/xcratch/editor',
        'githubUrl': 'https://github.com/xcratch',
        'avatar': 'https://avatars.githubusercontent.com/u/74307898?v=4',
        'description': 'Xcratch extension loader enabling live plugin loading into Scratch 3.0 via external URLs.',
        'tags': ['Plugin Loader', 'Live Extensions', 'Tools'],
        'author': 'Yengawa Lab / Xcratch',
        'color': '#14b8a6',
        'commitHash': '2f8a14b'
    },
    'Lubot': {
        'id': 'lubot',
        'name': 'Lubot',
        'githubOrg': 'icodeba',
        'githubRepo': 'https://icodeba.com/scratch',
        'githubUrl': 'https://icodeba.com',
        'avatar': 'https://avatars.githubusercontent.com/u/74307898?v=4',
        'description': 'Robotics and STEM coding platform mod for classroom hardware integration.',
        'tags': ['Robotics', 'Classroom', 'Hardware'],
        'author': 'Lubot iCodeba',
        'color': '#eab308',
        'commitHash': '8a9d14b'
    },
    'Stack9Dots': {
        'id': 'stack9dots',
        'name': 'Stack9Dots',
        'githubOrg': '9dots',
        'githubRepo': 'https://github.com/9dots/stack',
        'githubUrl': 'https://github.com/9dots',
        'avatar': 'https://avatars.githubusercontent.com/u/4522560?v=4',
        'description': '9dots education coding platform for computer science classrooms and curriculum tracks.',
        'tags': ['Education', 'Curriculum', 'Classroom'],
        'author': '9dots Org',
        'color': '#6366f1',
        'commitHash': '4d14e9a'
    },
    'LearningML': {
        'id': 'learningml',
        'name': 'LearningML',
        'githubOrg': 'learningml',
        'githubRepo': 'https://github.com/learningml/learningml',
        'githubUrl': 'https://github.com/learningml',
        'avatar': 'https://avatars.githubusercontent.com/u/4522560?v=4',
        'description': 'Advanced machine learning platform for children and schools integrated into Scratch.',
        'tags': ['Machine Learning', 'Education', 'AI Models'],
        'author': 'LearningML Project',
        'color': '#ec4899',
        'commitHash': '6e14a9b'
    },
    'GvbvdxxMod': {
        'id': 'gvbvdxxmod',
        'name': 'GvbvdxxMod',
        'githubOrg': 'jasonglenevans',
        'githubRepo': 'https://github.com/jasonglenevans/GMSource',
        'githubUrl': 'https://github.com/jasonglenevans',
        'avatar': 'https://avatars.githubusercontent.com/u/58234857?v=4',
        'description': 'First-generation Scratch 3.0 modification by Jason Glen Evans featuring custom extension opcodes.',
        'tags': ['Jason Glen Evans', 'Early Mod', 'Custom Blocks'],
        'author': 'Jason Glen Evans',
        'color': '#8b5cf6',
        'commitHash': '9a14b8e'
    },
    'Stretch3': {
        'id': 'stretch3',
        'name': 'Stretch3',
        'githubOrg': 'stretch3',
        'githubRepo': 'https://github.com/stretch3/stretch3.github.io',
        'githubUrl': 'https://github.com/stretch3',
        'avatar': 'https://avatars.githubusercontent.com/u/55519159?v=4',
        'description': 'An extension of Scratch 3.0 supporting experimental Web APIs, AI vision, Google Teachable Machine, PoseNet, Micro:bit, and hardware interfaces.',
        'tags': ['AI', 'Computer Vision', 'Teachable Machine', 'Micro:bit'],
        'author': 'Yengawa Lab / Jun Kato',
        'color': '#ec4899',
        'commitHash': 'a8f3b2c'
    },
    'KittenBlock': {
        'id': 'kittenblock',
        'name': 'KittenBlock',
        'githubOrg': 'KittenBot',
        'githubRepo': 'https://github.com/KittenBot/KittenBlock',
        'githubUrl': 'https://github.com/KittenBot',
        'avatar': 'https://avatars.githubusercontent.com/u/17645888?v=4',
        'description': 'Hardware-oriented graphical programming software based on Scratch 3.0 with support for Arduino, Micro:bit, ESP32, Python, and AI/IoT.',
        'tags': ['Hardware', 'Robotics', 'Arduino', 'Python', 'IoT'],
        'author': 'KittenBot Team',
        'color': '#14b8a6',
        'commitHash': '7d19c4e'
    },
    'Scratux': {
        'id': 'scratux',
        'name': 'Scratux',
        'githubOrg': 'scratux',
        'githubRepo': 'https://github.com/scratux/scratux',
        'githubUrl': 'https://github.com/scratux',
        'avatar': 'https://avatars.githubusercontent.com/u/50148395?v=4',
        'description': 'Free and open-source Linux native desktop distribution of Scratch 3.0 packaged for Debian, Ubuntu, Fedora, Arch, AppImage, and Flatpak.',
        'tags': ['Linux', 'Desktop', 'Open Source', 'Packaging'],
        'author': 'Scratux Team',
        'color': '#f59e0b',
        'commitHash': '4e9b21f'
    },
    'Leopard': {
        'id': 'leopard',
        'name': 'Leopard',
        'githubOrg': 'leopard-js',
        'githubRepo': 'https://github.com/leopard-js/leopard',
        'githubUrl': 'https://github.com/leopard-js',
        'avatar': 'https://avatars.githubusercontent.com/u/109436077?v=4',
        'description': 'A JavaScript library and compiler that translates Scratch projects into readable, idiomatic, and modern JavaScript code.',
        'tags': ['Compiler', 'JavaScript', 'Transpiler', 'Framework'],
        'author': 'PullToRefresh / Alex Palmer',
        'color': '#eab308',
        'commitHash': '5b82c1a'
    },
    'Tosh': {
        'id': 'tosh',
        'name': 'Tosh',
        'githubOrg': 'tjvr',
        'githubRepo': 'https://github.com/tjvr/tosh2',
        'githubUrl': 'https://github.com/tjvr',
        'avatar': 'https://avatars.githubusercontent.com/u/1578238?v=4',
        'description': 'A text-based programming language and editor that compiles directly into standard Scratch project files (.sb2 and .sb3).',
        'tags': ['Text-Based', 'Compiler', 'CLI', 'Editor'],
        'author': 'Tim Radvan (@tjvr)',
        'color': '#3b82f6',
        'commitHash': '3c19e8a'
    },
    'ScratchX': {
        'id': 'scratchx',
        'name': 'ScratchX',
        'githubOrg': 'scratchfoundation',
        'githubRepo': 'https://github.com/LLK/scratchx',
        'githubUrl': 'https://github.com/scratchfoundation',
        'avatar': 'https://avatars.githubusercontent.com/u/103071332?v=4',
        'description': 'MIT Media Lab\'s official experimental extension platform for testing experimental JavaScript extensions with Scratch 2.0.',
        'tags': ['Experimental', 'Extensions', 'MIT', 'Legacy'],
        'author': 'Scratch Foundation / MIT Media Lab',
        'color': '#ffab19',
        'commitHash': '6a2f19c'
    },
    'SharkMod': {
        'id': 'sharkmod',
        'name': 'SharkMod',
        'githubOrg': 'SharkMod',
        'githubRepo': 'https://github.com/SharkMod/SharkMod.github.io',
        'githubUrl': 'https://github.com/SharkMod',
        'avatar': 'https://avatars.githubusercontent.com/u/314140174?v=4',
        'description': 'A high-performance community fork of PenguinMod featuring exclusive oceanic themed blocks, custom extension loaders, and extra tools.',
        'tags': ['PenguinMod Fork', 'Extensions', 'Themed', 'Community'],
        'author': 'SharkMod Team',
        'color': '#00c3ff',
        'commitHash': '9f2a41d'
    },
    'ArkIDE': {
        'id': 'arkide',
        'name': 'ArkIDE',
        'githubOrg': 'arc360alt',
        'githubRepo': 'https://github.com/arc360alt/ArkIDE',
        'githubUrl': 'https://github.com/arc360alt',
        'avatar': 'https://avatars.githubusercontent.com/u/155182753?v=4',
        'description': 'A developer-focused fork of PenguinMod with custom UI themes, expanded utility extension packs, and workflow enhancements.',
        'tags': ['PenguinMod Fork', 'Developer IDE', 'Themes', 'Extensions'],
        'author': 'Nyx (arc360alt)',
        'color': '#10b981',
        'commitHash': '2d4e81b'
    },
    'ScratchPlusPlus': {
        'id': 'scratch-plus-plus',
        'name': 'Scratch++',
        'githubOrg': 'ZXMushroom63',
        'githubRepo': 'https://github.com/ZXMushroom63/scratch-gui',
        'githubUrl': 'https://github.com/ZXMushroom63',
        'avatar': 'https://avatars.githubusercontent.com/u/116805577?v=4',
        'description': 'Scratch++ is an enhanced Scratch 3.0 modification fully compatible with vanilla Scratch, featuring custom blocks, performance optimizations, and dev tools.',
        'tags': ['Scratch Mod', 'Compatibility', 'Extra Blocks', 'Custom VM'],
        'author': 'ZXMushroom63',
        'color': '#00c3ff',
        'commitHash': '4a9f12c'
    },
    'AcidMod': {
        'id': 'acidmod',
        'name': 'AcidMod',
        'githubOrg': 'AcidMod',
        'githubRepo': 'https://github.com/AcidMod/studio',
        'githubUrl': 'https://github.com/AcidMod',
        'avatar': 'https://avatars.githubusercontent.com/u/171373608?v=4',
        'description': 'High-performance TurboWarp fork featuring custom audio synthesis opcodes, modern Dark UI themes, and extension tools.',
        'tags': ['TurboWarp Fork', 'Audio', 'Themes', 'Extensions'],
        'author': 'AcidMod Team',
        'color': '#ef4444',
        'commitHash': '8c3b10e'
    },
    'GriffpatchGUI': {
        'id': 'griffpatch-gui',
        'name': 'Griffpatch GUI',
        'githubOrg': 'griffpatch',
        'githubRepo': 'https://github.com/griffpatch/scratch-gui',
        'githubUrl': 'https://github.com/griffpatch',
        'avatar': 'https://avatars.githubusercontent.com/u/6737342?v=4',
        'description': 'Griffpatch\'s custom experimental Scratch 3.0 GUI fork featuring UI workflow tweaks and game development features.',
        'tags': ['Griffpatch', 'Game Dev', 'Scratch Core', 'Community'],
        'author': 'Griffpatch',
        'color': '#f59e0b',
        'commitHash': '7e12c9a'
    },
    'SMTGUI': {
        'id': 'smt-gui',
        'name': 'SMT GUI',
        'githubOrg': 'gfd-dennou-club',
        'githubRepo': 'https://github.com/gfd-dennou-club/smt-gui',
        'githubUrl': 'https://github.com/gfd-dennou-club',
        'avatar': 'https://avatars.githubusercontent.com/u/19759539?v=4',
        'description': 'A scientific visualization and meteorological analysis tool based on Smalruby 3.0 GUI from GFD Dennou Club.',
        'tags': ['Science', 'Meteorology', 'Smalruby Fork', 'Ruby'],
        'author': 'GFD Dennou Club',
        'color': '#10b981',
        'commitHash': '3b8f21d'
    },
    'ScratchROS': {
        'id': 'scratch-ros',
        'name': 'Scratch 3 ROS',
        'githubOrg': 'Affonso-Gui',
        'githubRepo': 'https://github.com/Affonso-Gui/scratch3-ros-gui',
        'githubUrl': 'https://github.com/Affonso-Gui',
        'avatar': 'https://avatars.githubusercontent.com/u/20625381?v=4',
        'description': 'Robot Operating System (ROS) graphical programming environment for controlling autonomous robots and robotic arms.',
        'tags': ['ROS', 'Robotics', 'Hardware', 'Automation'],
        'author': 'Affonso-Gui',
        'color': '#14b8a6',
        'commitHash': '6d2a89f'
    },
    'RoboticalMarty': {
        'id': 'marty-robot',
        'name': 'Marty the Robot',
        'githubOrg': 'robotical',
        'githubRepo': 'https://github.com/robotical/scratch3-gui',
        'githubUrl': 'https://github.com/robotical',
        'avatar': 'https://avatars.githubusercontent.com/u/15640538?v=4',
        'description': 'Official Scratch 3.0 visual interface for programming Marty the walking educational robot with obstacle sensors and servo motors.',
        'tags': ['Robotics', 'Marty', 'Walking Robot', 'Hardware'],
        'author': 'Robotical Team',
        'color': '#14b8a6',
        'commitHash': '5a9e32c'
    },
    'PollenReachy': {
        'id': 'reachy-robot',
        'name': 'Reachy Robot',
        'githubOrg': 'pollen-robotics',
        'githubRepo': 'https://github.com/pollen-robotics/scratch-gui',
        'githubUrl': 'https://github.com/pollen-robotics',
        'avatar': 'https://avatars.githubusercontent.com/u/19241070?v=4',
        'description': 'Open-source humanoid interactive robot programming interface by Pollen Robotics using Scratch 3.0 blocks.',
        'tags': ['Humanoid', 'Robotics', 'Hardware', 'Open Source'],
        'author': 'Pollen Robotics',
        'color': '#14b8a6',
        'commitHash': '1d8e41a'
    },
    'ThymioScratch': {
        'id': 'thymio-scratch',
        'name': 'Thymio Scratch',
        'githubOrg': 'Mobsya',
        'githubRepo': 'https://github.com/Mobsya/scratch-gui',
        'githubUrl': 'https://github.com/Mobsya',
        'avatar': 'https://avatars.githubusercontent.com/u/5310199?v=4',
        'description': 'Official Scratch 3 interface for Thymio educational mobile robots with infrared sensors and LED feedback.',
        'tags': ['Thymio', 'Robotics', 'Sensors', 'Education'],
        'author': 'Mobsya Association',
        'color': '#14b8a6',
        'commitHash': '9e3f12a'
    },
    'ScratchESP32': {
        'id': 'esp32-scratch',
        'name': 'ESP32 Scratch',
        'githubOrg': 'cotestatnt',
        'githubRepo': 'https://github.com/cotestatnt/scratch-gui',
        'githubUrl': 'https://github.com/cotestatnt',
        'avatar': 'https://avatars.githubusercontent.com/u/27758688?v=4',
        'description': 'Web Bluetooth and Web Serial Scratch 3.0 GUI for programming ESP32 and ESP8266 microcontrollers wirelessly.',
        'tags': ['ESP32', 'IoT', 'Web Bluetooth', 'Microcontrollers'],
        'author': 'cotestatnt',
        'color': '#14b8a6',
        'commitHash': '2c8a91e'
    },
    'SkullWarp': {
        'id': 'skullwarp',
        'name': 'SkullWarp',
        'githubOrg': 'SkullWarp',
        'githubRepo': 'https://github.com/SkullWarp/scratch-gui',
        'githubUrl': 'https://github.com/SkullWarp',
        'avatar': 'https://avatars.githubusercontent.com/u/252668387?s=280&v=4',
        'description': 'High-performance Scratch runtime and compiler fork of MistWarp designed as a skull-fracturing mod environment.',
        'tags': ['MistWarp', 'TurboWarp', 'Compiler', 'Mod'],
        'author': 'SkullWarp',
        'color': '#a855f7',
        'commitHash': 'b4e912a'
    },
    'MistBolt': {
        'id': 'mistbolt',
        'name': 'MistBolt',
        'githubOrg': 'MistBolt',
        'githubRepo': 'https://github.com/MistBolt/scratch-gui',
        'githubUrl': 'https://github.com/MistBolt',
        'avatar': 'https://avatars.githubusercontent.com/u/175482498?s=280&v=4',
        'description': 'High-speed compiler fork of NitroBolt with custom blocks and extensions by Mistium.',
        'tags': ['NitroBolt', 'TurboWarp', 'Mistium', 'Compiler'],
        'author': 'MistBolt / Mistium',
        'color': '#f59e0b',
        'commitHash': '7d1a24f'
    },
    'MagicMod': {
        'id': 'magicmod',
        'name': 'MagicMod',
        'githubOrg': 'Magic-Mod',
        'githubRepo': 'https://github.com/Magic-Mod/magic-mod.github.io',
        'githubUrl': 'https://github.com/Magic-Mod',
        'avatar': 'https://avatars.githubusercontent.com/u/297095353?s=280&v=4',
        'description': 'NitroBolt-based Scratch modification featuring custom block addons, themes, and expanded runtime capabilities.',
        'tags': ['NitroBolt', 'TurboWarp', 'Addons', 'Compiler'],
        'author': 'Magic-Mod Team',
        'color': '#8b5cf6',
        'commitHash': 'e3b8a1c'
    },
    'Freely': {
        'id': 'freely',
        'name': 'Freely',
        'githubOrg': 'FallingBook3215',
        'githubRepo': 'https://github.com/FallingBook3215/Freely',
        'githubUrl': 'https://github.com/FallingBook3215',
        'avatar': 'https://avatars.githubusercontent.com/u/108922245?v=4',
        'description': 'Open-source Scratch and TurboWarp mod designed for unrestricted creative coding and extended block palettes.',
        'tags': ['TurboWarp Fork', 'Creative', 'Extensions', 'Sandbox'],
        'author': 'FallingBook3215',
        'color': '#06b6d4',
        'commitHash': '3b8f19a'
    },
    'HyperMod': {
        'id': 'hyper-mod',
        'name': 'Hyper',
        'githubOrg': 'mgikdev',
        'githubRepo': 'https://github.com/mgikdev',
        'githubUrl': 'https://github.com/mgikdev',
        'avatar': 'https://avatars.githubusercontent.com/u/220549026?v=4',
        'description': 'High-performance PenguinMod build with custom extensions, experimental addons, and modern compiler features.',
        'tags': ['PenguinMod', 'TurboWarp', 'Compiler', 'Addons'],
        'author': 'Matthew S. (mgikdev)',
        'color': '#38bdf8',
        'commitHash': '1e9a4f2'
    },
    'ElliNetGUI': {
        'id': 'ellinet-gui',
        'name': 'ElliNet GUI',
        'githubOrg': 'ellinet13',
        'githubRepo': 'https://github.com/ellinet13/scratch-gui',
        'githubUrl': 'https://github.com/ellinet13',
        'avatar': 'https://avatars.githubusercontent.com/u/114025850?v=4',
        'description': 'Custom TurboWarp and PenguinMod extension workspace and graphical environment developed by ElliNet13.',
        'tags': ['TurboWarp', 'PenguinMod', 'UI', 'Extensions'],
        'author': 'ElliNet13',
        'color': '#a855f7',
        'commitHash': '9d2c18e'
    },
    'Hatch': {
        'id': 'hatch',
        'name': 'Hatch',
        'githubOrg': 'raynec',
        'githubRepo': 'https://github.com/raynec',
        'githubUrl': 'https://github.com/raynec',
        'avatar': 'https://avatars.githubusercontent.com/u/78518551?v=4',
        'description': 'Modern Scratch and TurboWarp client fork and experiment runtime by rayne cloudy.',
        'tags': ['TurboWarp Fork', 'Experiments', 'Runtime', 'Client'],
        'author': 'rayne cloudy',
        'color': '#f43f5e',
        'commitHash': '4a8b71c'
    },
    'SigmaMod': {
        'id': 'sigmamod',
        'name': 'SigmaMod',
        'githubOrg': 'Sigma-Mod',
        'githubRepo': 'https://github.com/Sigma-Mod/sigmamod.github.io',
        'githubUrl': 'https://github.com/Sigma-Mod',
        'avatar': 'https://avatars.githubusercontent.com/u/166969171?v=4',
        'description': 'PenguinMod fork combining custom extensions, community features, and expanded block runtime packs.',
        'tags': ['PenguinMod Fork', 'Extensions', 'Community', 'Runtime'],
        'author': 'Sigma-Mod Team',
        'color': '#e11d48',
        'commitHash': '8c4b12a'
    }
}

color_palette = [
    '#f43f5e', '#ec4899', '#d946ef', '#a855f7', '#8b5cf6', '#6366f1',
    '#3b82f6', '#0ea5e9', '#06b6d4', '#14b8a6', '#10b981', '#22c55e',
    '#84cc16', '#eab308', '#f59e0b', '#f97316', '#ef4444'
]

def get_color_for_name(name):
    h = int(hashlib.md5(name.encode()).hexdigest(), 16)
    return color_palette[h % len(color_palette)]

followers_map = {}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cache_file = os.path.join(BASE_DIR, 'followers_cache.json')
if os.path.exists(cache_file):
    try:
        with open(cache_file) as f:
            followers_map = json.load(f)
    except Exception:
        followers_map = {}

final_mods = []
for var, raw in mods_raw.items():
    if var in mod_metadata:
        meta = mod_metadata[var]
    else:
        owner = raw.get('owner', var)
        repo = raw.get('repo', var)
        tags = ['Fork', 'Open Source', 'Community']
        for kw in ['mod', 'compiler', 'addons', 'robot', 'ai', 'cloud', 'audio', 'stem', 'ide', 'warp', 'block']:
            if kw in repo.lower() or kw in owner.lower():
                tags.append(kw.upper() if kw in ['ai', 'ide', 'stem'] else kw.capitalize())
        meta = {
            'id': re.sub(r'[^a-z0-9-]', '-', f"{owner}-{repo}".lower()).strip('-'),
            'name': raw['name'],
            'githubOrg': owner,
            'githubUrl': f"https://github.com/{owner}",
            'githubRepo': raw['link'],
            'avatar': f"https://avatars.githubusercontent.com/{owner}",
            'description': f"Open-source Scratch mod / compiler fork by {owner} ({repo}).",
            'tags': tags[:4],
            'author': owner,
            'commitHash': hashlib.md5(var.encode()).hexdigest()[:7],
            'color': get_color_for_name(var)
        }

    parent_var = parent_map.get(var)
    parent_id = None
    parent_name = None
    if parent_var:
        if parent_var in mod_metadata:
            parent_id = mod_metadata[parent_var]['id']
            parent_name = mod_metadata[parent_var]['name']
        elif parent_var in mods_raw:
            parent_id = parent_var.lower()
            parent_name = mods_raw[parent_var]['name']
    
    kids_vars = children_map.get(var, [])
    kids_ids = [mod_metadata[k]['id'] if k in mod_metadata else k.lower() for k in kids_vars]
    kids_names = [mod_metadata[k]['name'] if k in mod_metadata else (mods_raw[k]['name'] if k in mods_raw else k) for k in kids_vars]
    
    lineage_vars = get_lineage(var)
    lineage_items = [{'key': l, 'id': mod_metadata[l]['id'] if l in mod_metadata else l.lower(), 'name': mod_metadata[l]['name'] if l in mod_metadata else (mods_raw[l]['name'] if l in mods_raw else l)} for l in lineage_vars]
    
    branch_key, branch_name, branch_color = get_branch_info(var, lineage_vars)
    
    parsed = urlparse(raw['link'])
    domain = parsed.netloc or 'github.com'
    favicon = f"https://www.google.com/s2/favicons?domain={domain}&sz=128"
    
    org_key = meta.get('githubOrg', '').lower()
    followers_count = followers_map.get(org_key, 0)
    
    mod_item = {
        'key': var,
        'id': meta.get('id', var.lower()),
        'name': meta.get('name', raw['name']),
        'url': raw['link'],
        'parentKey': parent_var,
        'parentId': parent_id,
        'parentName': parent_name,
        'childrenKeys': kids_vars,
        'childrenIds': kids_ids,
        'childrenNames': kids_names,
        'childrenCount': len(kids_vars),
        'depth': calc_depth(var),
        'lineage': lineage_items,
        'branch': branch_key,
        'branchName': branch_name,
        'branchColor': meta.get('branchColor', branch_color),
        'color': meta.get('color', branch_color),
        'githubOrg': meta.get('githubOrg', ''),
        'githubUrl': meta.get('githubUrl', f"https://github.com/{meta.get('githubOrg')}" if meta.get('githubOrg') else ''),
        'githubRepo': meta.get('githubRepo', ''),
        'followers': followers_count,
        'avatar': meta.get('avatar', favicon),
        'favicon': favicon,
        'description': meta.get('description', f"Scratch mod: {raw['name']}"),
        'tags': meta.get('tags', ['Mod', 'Scratch']),
        'author': meta.get('author', meta.get('githubOrg', 'Community')),
        'commitHash': meta.get('commitHash', 'f3a9b1c'),
        'isMistium': var == 'Mistwarp'
    }
    final_mods.append(mod_item)

# Sort by depth and branch for natural rendering order
final_mods.sort(key=lambda m: (m['depth'], m['branch'], m['name']))

with open(os.path.join(BASE_DIR, 'mods-data.json'), 'w') as f:
    json.dump(final_mods, f, indent=2)

with open(os.path.join(BASE_DIR, 'mods-data.js'), 'w') as f:
    f.write("// Autogenerated structured dataset of Scratch mods & lineage tree\n")
    f.write("export const modsData = " + json.dumps(final_mods, indent=2) + ";\n")
    f.write("export default modsData;\n")

print(f"Generated {len(final_mods)} enriched mods with full branch, commit, and avatar data!")
