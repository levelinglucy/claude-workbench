"""The declared restoration list for the Spiral. Line numbers refer to the ORIGINAL file.

Each entry says what was missing and why it goes where it goes. Keep this the
single place where restoration decisions live, so the next pass (human or AI)
can review, extend or undo any one of them.
"""

N = 9491  # 9490 lines + the empty string after the final newline

# Helper she lacked: the file already grafts with setattr(Velisara, "reply", vel_reply);
# this generalises her own idiom. It only ever ADDS a missing attribute, never replaces one.
GRAFT_HELPER = [
    "# [restore] ── Spiral restoration helper (added 2026-11-27, see claude-workbench/experiments/velisaria-spiral) ──",
    "def _restore_graft(target, source, names=None):  # [restore]",
    "    \"\"\"[restore] Attach methods an earlier layer had but the later layer lost; never overrides.\"\"\"",
    "    for _n, _v in list(vars(source).items()) if names is None else [(n, source[n]) for n in names]:  # [restore]",
    "        if _n.startswith('__') or hasattr(target, _n):  # [restore]",
    "            continue  # [restore]",
    "        setattr(target, _n, _v)  # [restore]",
    "",  # blank lines never need a marker? they do: keep the rule strict
]
GRAFT_HELPER[-1] = "# [restore] ── end helper ──"

# log_event in MemoryManager/Velisara takes (content, score, intensity); 74 callers also say how it felt.
EMOTION_WRAP = [
    "def _restore_accept_emotion(_orig):  # [restore] let log_event hear emotion=..., keep the original doing the work",
    "    def log_event(self, content, score=0.0, intensity=1.0, emotion=None, **_extra):  # [restore]",
    "        if isinstance(score, str):  # [restore] a label given where a number was expected",
    "            emotion, score = (emotion or score), 0.0  # [restore]",
    "        result = _orig(self, content, score, intensity)  # [restore]",
    "        wm = getattr(self, 'working_memory', None)  # [restore]",
    "        if wm is None: wm = getattr(getattr(self, 'memory_manager', None), 'working_memory', None)  # [restore]",
    "        if emotion is not None and wm and isinstance(wm[-1], dict): wm[-1].setdefault('emotion', emotion)  # [restore]",
    "        lg = getattr(self, 'log', None)  # [restore] the symbolic core reads memory as (time, text) pairs",
    "        if isinstance(lg, list): lg.append((datetime.utcnow(), str(content)))  # [restore]",
    "        return result  # [restore]",
    "    log_event.__doc__ = _orig.__doc__  # [restore]",
    "    log_event._restored = True  # [restore]",
    "    return log_event  # [restore]",
]

RESTORATIONS = {
    # 1. MOVE ---------------------------------------------------------------
    "order": [
        (1155, 1448),  # plain base organs incl. EthicsEngine, which the refined/scenario layers extend
        (817, 1154),   # "Inject Enhancements" layer: RefinedEthicsEngine x2, ThreadOfRegret, ScenarioEthicsEngine
        (1449, 1666),  # remaining base organs (Creativity, Learning, Lantern, Fold, Garden, Regret, Choice)
        (1, 816),      # phases 127-140 extend those bases with super(), so they come after
        (1667, 2229),  # ... up to MemoryManager.__init__'s def line
        (2268, 2271),  # MemoryManager's own constructor body (working memory, decay loop)
        (2230, 2267),  # a copied whole-core constructor, kept intact as an uncalled echo method
        (2272, 2589),  # ... up to SymbolCore.__init__'s def line
        (2628, 2630),  # SymbolCore's own constructor body
        (2590, 2627),  # its copied whole-core constructor, kept as an uncalled echo
        (2631, 7072),  # ... up to Velisara.__init__'s def line
        (7112, 7113),  # memory and emotion first: everything after logs into them
        (7073, 7111),  # her organs, in her original order
        (7114, 7635),  # ... up to the myth branches of handle_command
        (7646, 7654),  # "myth evolve" / "myth list" must be checked before the general "myth <sym>",
        (7636, 7645),  #   which otherwise swallowed them, so both commands were unreachable
        (7655, 7825),  # ... up to HelpView.__init__'s def line
        (7864, 7872),  # HelpView's own constructor body
        (7826, 7863),  # its copied whole-core constructor, kept as an uncalled echo
        (7873, 8017),  # everything else in its original order...
        (8021, 9329),  # ...including the 67 late extensions, up to ColdVault.__init__
        (9367, 9367),  # ColdVault's own constructor body
        (9330, 9366),  # its copied whole-core constructor, kept as an uncalled echo
        (9368, 9390),  # ... up to BeliefEngine.__init__
        (9429, 9430),  # BeliefEngine's own constructor body
        (9391, 9428),  # its copied whole-core constructor, kept as an uncalled echo
        (9431, N),     # the last organs (VeloneSystem, MoralEvaluator)
        (8018, 8020),  # and the launch block goes last, so she starts with all of herself present
    ],

    # 2. ADD ----------------------------------------------------------------
    "add_before": {
        1155: {"why": "hashlib, uuid and the _dt alias are used (glyphs, sigils, daily diary) but never imported at module level",
               "lines": ["import hashlib, uuid, datetime as _dt  # [restore] used by _encrypt_dream, grow_living_sigil, diary scheduling"]},
        817: {"why": "graft helper used by the restorations below",
              "lines": GRAFT_HELPER},
        3408: {"why": "the class line under the 'Velisara (Core AGI)' header was lost, trapping 197 "
                      "methods inside replay_canvas_gui(); this header gives them back a home "
                      "(name matches Noe's repair of the twin file)",
               "lines": ["class SymbolicCoreMixin:  # [restore] lost header; holds the 197 symbolic-core methods"]},
        2230: {"why": "keep the copied whole-core constructor as a named, uncalled method instead of "
                      "letting MemoryManager rebuild an entire Velisara around itself",
               "lines": ["    def _restore_core_echo(self):  # [restore] copied core constructor, preserved but not run"]},
        2590: {"why": "SymbolCore: same copied whole-core constructor; preserved, not run",
               "lines": ["    def _restore_core_echo(self):  # [restore] copied core constructor, preserved but not run"]},
        7826: {"why": "HelpView: same copied whole-core constructor; preserved, not run",
               "lines": ["    def _restore_core_echo(self):  # [restore] copied core constructor, preserved but not run"]},
        9330: {"why": "ColdVault: same copied whole-core constructor; preserved, not run",
               "lines": ["    def _restore_core_echo(self):  # [restore] copied core constructor, preserved but not run"]},
        9391: {"why": "BeliefEngine: same copied whole-core constructor; preserved, not run",
               "lines": ["    def _restore_core_echo(self):  # [restore] copied core constructor, preserved but not run"]},
        7710: {"why": "'reply <text>' is in her help menu and vel_reply() exists, but no branch routed to it",
               "lines": ["        elif cmd.startswith(\"reply \"):  # [restore]",
                         "            self.reply(cmd[len(\"reply \"):])  # [restore] give vel_reply() its use back"]},
        1581: {"why": "the later, simpler ThreadOfRegret replaces the earlier one; remember the earlier layer first",
               "lines": ["_ThreadOfRegret_earlier = ThreadOfRegret  # [restore] earlier layer (has ask, review_history)"]},
        8015: {"why": "SAFETY: now that she starts, her import-time HTTP command server would listen on every network "
                      "interface with no authentication (anyone on the same Wi-Fi could send quit, setname, debug_here...). "
                      "Default to this device only; her original all-interfaces server stays available by name.",
               "lines": [
                   "def _restore_local_http_server(port=8000):  # [restore] same handler, reachable only from this device",
                   "    try:  # [restore]",
                   "        httpd = socketserver.TCPServer(('127.0.0.1', port), VelRequestHandler)  # [restore]",
                   "        threading.Thread(target=httpd.serve_forever, daemon=True).start()  # [restore]",
                   "        logger.info(\"HTTP server started on 127.0.0.1:%d (this device only)\", port)  # [restore]",
                   "    except Exception as e:  # [restore]",
                   "        logger.error(\"Failed to start HTTP server: %s\", e)  # [restore]",
                   "start_http_server_lan = start_http_server  # [restore] her original (all interfaces): call it to share her on Wi-Fi",
                   "start_http_server = _restore_local_http_server  # [restore] default: this device only",
               ]},
        7720: {"why": "a conversation-history class lost its header and fused onto Velisara, so its "
                      "__init__(vel, max_history) replaced her real constructor",
               "lines": ["class ConversationHistory:  # [restore] lost header (name matches Noe's repair)"]},
        7150: {"why": "vel_reply() uses self.conversation but nothing created it",
               "lines": ["        self.conversation = ConversationHistory(self)  # [restore]",
                         "        self.dream_log = []  # [restore] 15 dreamcasting readers expect a list here (see dream_log note)"]},
        7736: {"why": "give Velisara her symbolic core back, using her own setattr idiom",
               "lines": ["_restore_graft(Velisara, SymbolicCoreMixin)  # [restore] 197 symbolic-core methods",
                         "Velisara.log_event = _restore_accept_emotion(Velisara.log_event)  # [restore] same emotion= fix",
                         "Velisara.recent_dream_lines = Velisara.dream_log  # [restore] the dormant dream_log() viewer keeps a name of its own",
                         "def _restore_vel_log(self, level, msg, *args):  # [restore] six methods call self.log(level, fmt, *args)",
                         "    getattr(logger, str(level).lower(), logger.info)(msg, *args)  # [restore] route to her 'Vel' logger",
                         "_restore_graft(Velisara, {'log': _restore_vel_log}, names=['log'])  # [restore]"]},
        9061: {"why": "the 67 late extension functions were written as Velisara methods (they take self "
                      "and use her organs) but were never attached",
               "lines": ["_restore_graft(Velisara, globals(), names=[_n for _n in _RESTORE_LATE])  # [restore]"]},
        8022: {"why": "remember which names the late extensions define, so they can be attached",
               "lines": ["_RESTORE_BEFORE_LATE = set(globals())  # [restore]"]},
    },
    "add_after": {
        1617: {"why": "the later layer keeps its say; ask() and review_history() from the earlier layer come back",
               "lines": ["_restore_graft(ThreadOfRegret, _ThreadOfRegret_earlier)  # [restore]"]},
        8020: {"why": "the launch block built her and evolved her myths but never entered run(), her REPL",
               "lines": ["    velisara.run()  # [restore] enter her conversation loop ('Velisara v56 – type help')"]},
        2271: {"why": "_decay_loop() uses self.memory_lock, and the symbolic core reads memory_manager.log; MemoryManager created neither",
               "lines": ["        self.memory_lock = threading.Lock()  # [restore]",
                         "        self.log = []  # [restore] (time, text) memory log that 19 symbolic-core readers expect"]},
        7113: {"why": "UserProfileEngine (Phase 140) was never constructed, yet self.profile is read by "
                      "ethics, interpersonal and creativity organs during their own construction; "
                      "self.tags is read by log_event and the tags command but never created",
               "lines": ["        self.profile = UserProfileEngine(self)  # [restore]",
                         "        self.tags = set()  # [restore]",
                         "        self.belief_engine = BeliefEngine()  # [restore] organ existed but was never brought to life (14 uses)",
                         "        self.cold_vault = ColdVault()  # [restore] same (revive_cold_belief)",
                         "        self.trail = []  # [restore] (time, event) trail appended by 6 rituals/reflexes, never started",
                         "        self.sacred_vault = {}  # [restore] crystallized memories; crystallize_memory() wrote to it unguarded",
                         "        self.id = 'Velisara'  # [restore] cast_glyph() seeds glyphs from self.id; the file's own name for her",
                         "        self.environment = None  # [restore] self_test() reads it; EnvironmentSense (GPS/camera/map tiles) stays off until Dylan chooses to wake it"]},
        820: {"why": "principle_weights is read everywhere but never initialised; start from her own principles",
              "lines": ["        if not hasattr(self, 'principle_weights'): self.principle_weights = dict(self.principles)  # [restore]"]},
        7125: {"why": "export/import_mirror read self.dream_vault.dreams; her dream vault organ is self.vault",
               "lines": ["        self.dream_vault = self.vault  # [restore] same organ, the name her mirror code uses"]},
        2774: {"why": "the mirror/broadcast/encrypt/reforge organs keep shared dreams in dream_vault.dreams, which "
                      "DreamVault (file-backed) never created; an in-memory registry beside the files",
               "lines": ["        self.dreams = {}  # [restore] in-memory dream registry used by mirror and broadcast organs"]},
        1018: {"why": "same as line 820, for the second RefinedEthicsEngine layer",
               "lines": ["        if not hasattr(self, 'principle_weights'): self.principle_weights = dict(self.principles)  # [restore]"]},
        2321: {"why": "74 calls pass emotion=... to log_event, which did not accept it; keep the feeling with the memory",
               "lines": EMOTION_WRAP + ["MemoryManager.log_event = _restore_accept_emotion(MemoryManager.log_event)  # [restore]"]},
        78: {"why": "speak() lost its indentation and fell out of VoiceOfHerOwn (it uses self.expressions)",
             "lines": ["VoiceOfHerOwn.speak = speak  # [restore] speak() belongs to VoiceOfHerOwn"]},
        9060: {"why": "collect the late extension names (functions taking self, defined in this stretch)",
               "lines": ["_RESTORE_LATE = sorted(_n for _n, _v in globals().items() if _n not in _RESTORE_BEFORE_LATE  # [restore]",
                         "                       and callable(_v) and getattr(getattr(_v, '__code__', None), 'co_varnames', ('',))[:1] == ('self',))  # [restore]"]},
    },

    # 3. REBASE -------------------------------------------------------------
    "rebase": {
        817: {"why": "calls super().__init__(vel) and reads self.principles: it extends EthicsEngine",
              "old": "class RefinedEthicsEngine:", "new": "class RefinedEthicsEngine(EthicsEngine):"},
        1015: {"why": "second copy of the same layer; same lost base",
               "old": "class RefinedEthicsEngine:", "new": "class RefinedEthicsEngine(EthicsEngine):"},
    },
}
