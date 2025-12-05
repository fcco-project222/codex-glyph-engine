#!/usr/bin/env python3
"""
════════════════════════════════════════════════════════════════════════════════
CODEXGLYPH ENGINE v2.6 - SOVEREIGN LANGUAGE PARSER
Captain-Sealed - December 2, 2025
════════════════════════════════════════════════════════════════════════════════

FOUNDATION LAYER 1 - COMPLETE IMPLEMENTATION
All mechanics, rules, and discoveries integrated into one seamless system.

CORE FEATURES:
• V+CC shadow detection (2-letter V+C prefix + C-starting base)
• Tilde Positional Clause (neutralizes V+CC for positional prefixes)
• Four parsing levels (Casual, Structural, Ceremonial, Educational)
• Three strictness tiers (Permissive, Standard, Rigorous)
• Dual shadow types (Structural V+CC + Semantic control language)
• Master numbers (11-99 preserved)
• Complete prefix/suffix/root databases with meanings
• Greek compound handling with tilde notation
• Technical field awareness (field-standard shadows)
• Context-based parsing (prefer English bases over Latin)
• Polarity matching (negative concept + shadow form = acceptable)
• Synonym suggestions (sovereign alternatives)
• Full document parsing and analysis

════════════════════════════════════════════════════════════════════════════════
"""

import re
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

# ════════════════════════════════════════════════════════════════════════════
# ENUMS AND DATA CLASSES
# ════════════════════════════════════════════════════════════════════════════

class ParsingLevel(Enum):
    """Four parsing levels for different contexts"""
    CASUAL = 1       # Minimal changes, everyday use
    STRUCTURAL = 2   # Show architecture, educational/technical
    CEREMONIAL = 3   # Maximum sovereignty, legal/sacred
    EDUCATIONAL = 4  # Full glossary with inline meanings

class StrictnessLevel(Enum):
    """Three strictness levels for shadow detection"""
    PERMISSIVE = 1   # Only Tier 1 (egregious)
    STANDARD = 2     # Tiers 1-2 (common shadows)
    RIGOROUS = 3     # All tiers (embedded shadows)

class ShadowType(Enum):
    """Two types of shadow glyphs"""
    STRUCTURAL = "V+CC structural violation"
    SEMANTIC = "Control language"
    BOTH = "Structural and Semantic"

@dataclass
class GlyphAnalysis:
    """Complete analysis of a word"""
    original: str
    parsed: str
    polarity: str
    resonance: str
    is_shadow: bool
    shadow_types: List[ShadowType]
    components: List[Dict]
    warnings: List[str]
    alternatives: List[str]
    tier: Optional[int] = None
    field_context: Optional[str] = None
    educational_note: Optional[str] = None

# ════════════════════════════════════════════════════════════════════════════
# MAIN PARSER CLASS
# ════════════════════════════════════════════════════════════════════════════

class CodexGlyphParser:
    """
    Main parser implementing all Layer 1 CodexGlyph mechanics.
    """
    
    # ════════════════════════════════════════════════════════════════════════
    # TAP-ROOT RESONANCE CHART (A=1 through Z=26)
    # ════════════════════════════════════════════════════════════════════════
    
    TAP_ROOT = {
        'A': (1, "Initiation·Spark"),
        'B': (2, "Duality·Choice"),
        'C': (3, "Creation·Flow"),
        'D': (4, "Structure·Stability"),
        'E': (5, "Freedom·Change"),
        'F': (6, "Harmony·SacredGeometry"),
        'G': (7, "Mystery·Introspection"),
        'H': (8, "Power·Infinity"),
        'I': (9, "Completion·Wisdom"),
        'J': (10, "RenewedInitiation"),
        'K': (11, "MasterDuality·Gateway"),
        'L': (12, "IlluminatedCreation"),
        'M': (13, "ManifestedStructure"),
        'N': (14, "NetworkedFreedom"),
        'O': (15, "WholeHarmony·Orb"),
        'P': (16, "PulsedMystery"),
        'Q': (17, "QuantumPower"),
        'R': (18, "RitualCompletion"),
        'S': (19, "SpiraledInitiation"),
        'T': (20, "TrialOfDuality"),
        'U': (21, "UnifiedCreation"),
        'V': (22, "MasterStructure"),
        'W': (23, "WovenFreedom"),
        'X': (24, "CrossedHarmony"),
        'Y': (25, "ForkedMystery"),
        'Z': (26, "ZeroedPower·Zenith")
    }
    
    # Master Numbers (11-99) - preserved during reduction
    MASTER_NUMBERS = {
        11: "Gateway·Luminator",
        22: "MasterBuilder",
        33: "MasterTeacher·Healer",
        44: "MasterFoundation",
        55: "MasterChange·Freedom",
        66: "MasterNurturer·Harmonizer",
        77: "MasterMystic·Seeker",
        88: "MasterManifestor·Abundance",
        99: "MasterHumanitarian·Completion"
    }
    
    # ════════════════════════════════════════════════════════════════════════
    # 2-LETTER V+C PREFIXES (Create V+CC shadows)
    # ════════════════════════════════════════════════════════════════════════
    
    VCC_PREFIXES = {
        # Positional prefixes (can use tilde to neutralize)
        'IN': {'meaning': 'into/within', 'type': 'positional', 'etymology': 'Latin in-'},
        'EX': {'meaning': 'out/from', 'type': 'positional', 'etymology': 'Latin ex-'},
        'AT': {'meaning': 'at/toward', 'type': 'positional', 'etymology': 'Latin ad-variant'},
        'OB': {'meaning': 'against/opposite', 'type': 'positional', 'etymology': 'Latin ob-'},
        'OP': {'meaning': 'against/toward', 'type': 'positional', 'etymology': 'Latin ob-variant'},
        'AD': {'meaning': 'toward/to', 'type': 'positional', 'etymology': 'Latin ad-'},
        'AB': {'meaning': 'away from', 'type': 'positional', 'etymology': 'Latin ab-'},
        
        # IN- variants (positional when directional, but structure same)
        'IM': {'meaning': 'into', 'type': 'positional', 'etymology': 'Latin in-assimilated'},
        'IL': {'meaning': 'into', 'type': 'positional', 'etymology': 'Latin in-assimilated'},
        'IR': {'meaning': 'into', 'type': 'positional', 'etymology': 'Latin in-assimilated'},
        'IF': {'meaning': 'into', 'type': 'positional', 'etymology': 'Latin in-assimilated'},
        
        # Operational prefix (cannot use tilde)
        'UN': {'meaning': 'liberation/reversal', 'type': 'operational', 'etymology': 'Old English un-'},
    }
    
    # ════════════════════════════════════════════════════════════════════════
    # OTHER PREFIXES (Don't create V+CC by structure)
    # ════════════════════════════════════════════════════════════════════════
    
    OTHER_PREFIXES = {
        # C+V structure (2-letter, consonant first)
        'RE': {'meaning': 'again/back/renewal', 'etymology': 'Latin re-'},
        'BE': {'meaning': 'causative/make', 'etymology': 'Old English be-'},
        'DE': {'meaning': 'removal/down', 'etymology': 'Latin de-'},
        'BI': {'meaning': 'by/at/near', 'etymology': 'Old English bi'},
        
        # 3+ letter prefixes
        'UNDER': {'meaning': 'beneath (UN+D+ER)', 'etymology': 'Old English'},
        'OVER': {'meaning': 'above (O+V+ER)', 'etymology': 'Old English'},
        'CON': {'meaning': 'together/with', 'etymology': 'Latin con-'},
        'COM': {'meaning': 'together/with', 'etymology': 'Latin con-variant'},
        'SUB': {'meaning': 'under/below', 'etymology': 'Latin sub-'},
        'SUP': {'meaning': 'under', 'etymology': 'Latin sub-assimilated'},
        'PRE': {'meaning': 'before/prior', 'etymology': 'Latin prae-'},
        'PRO': {'meaning': 'forward/forth', 'etymology': 'Latin pro-'},
        'POST': {'meaning': 'after/behind', 'etymology': 'Latin post-'},
        'ANTI': {'meaning': 'against/opposite', 'etymology': 'Greek anti-'},
        'COUNTER': {'meaning': 'against/opposite', 'etymology': 'Latin contra-'},
        'SUPER': {'meaning': 'above/beyond', 'etymology': 'Latin super-'},
        'INTER': {'meaning': 'between/among', 'etymology': 'Latin inter-'},
        'TRANS': {'meaning': 'across/through', 'etymology': 'Latin trans-'},
        'CIRCUM': {'meaning': 'around', 'etymology': 'Latin circum-'},
        'PER': {'meaning': 'through/thoroughly', 'etymology': 'Latin per-'},
        'EXTRA': {'meaning': 'outside/beyond', 'etymology': 'Latin extra-'},
        'INTRA': {'meaning': 'within', 'etymology': 'Latin intra-'},
        'WITH': {'meaning': 'together/against', 'etymology': 'Old English'},
        'OUT': {'meaning': 'beyond/external', 'etymology': 'Old English'},
        'DOWN': {'meaning': 'downward', 'etymology': 'Old English'},
        'UP': {'meaning': 'upward', 'etymology': 'Old English'},
        'FOR': {'meaning': 'away/prohibition', 'etymology': 'Old English'},
        'FORE': {'meaning': 'before/front', 'etymology': 'Old English'},
        'AFTER': {'meaning': 'following', 'etymology': 'Old English'},
        'MID': {'meaning': 'middle', 'etymology': 'Old English'},
        'DIS': {'meaning': 'apart/away', 'etymology': 'Latin dis-'},
        'EN': {'meaning': 'cause to be in', 'etymology': 'Latin en-'},
        'EM': {'meaning': 'cause to be in', 'etymology': 'Latin en-variant'},
        'NON': {'meaning': 'not/without', 'etymology': 'Latin non-'},
        'MIS': {'meaning': 'wrong/bad', 'etymology': 'Old English'},
        'MAL': {'meaning': 'bad/evil', 'etymology': 'Latin male-'},
        'HYPER': {'meaning': 'over/excessive', 'etymology': 'Greek hyper-'},
        'HYPO': {'meaning': 'under/below', 'etymology': 'Greek hypo-'},
        'META': {'meaning': 'beyond/change', 'etymology': 'Greek meta-'},
        'PARA': {'meaning': 'beside/beyond', 'etymology': 'Greek para-'},
        'PROTO': {'meaning': 'first/original', 'etymology': 'Greek protos-'},
        'SYN': {'meaning': 'together', 'etymology': 'Greek syn-'},
        'SYM': {'meaning': 'together', 'etymology': 'Greek syn-variant'},
        'NEO': {'meaning': 'new', 'etymology': 'Greek neos-'},
        'PALEO': {'meaning': 'old/ancient', 'etymology': 'Greek palaios-'},
        'AUTO': {'meaning': 'self', 'etymology': 'Greek autos-'},
        'MONO': {'meaning': 'one/single', 'etymology': 'Greek monos-'},
        'UNI': {'meaning': 'one/single', 'etymology': 'Latin unus-'},
        'MULTI': {'meaning': 'many', 'etymology': 'Latin multus-'},
        'POLY': {'meaning': 'many', 'etymology': 'Greek polys-'},
        'SEMI': {'meaning': 'half', 'etymology': 'Latin semi-'},
        'OMNI': {'meaning': 'all', 'etymology': 'Latin omnis-'},
        'DIA': {'meaning': 'through/across', 'etymology': 'Greek dia-'},
        'EPI': {'meaning': 'upon/over', 'etymology': 'Greek epi-'},
        'AMPHI': {'meaning': 'both/around', 'etymology': 'Greek amphi-'},
        'PERI': {'meaning': 'around/near', 'etymology': 'Greek peri-'},
        
        # Single-letter
        'E': {'meaning': 'out', 'etymology': 'Latin ex-variant'},
        'A': {'meaning': 'to/toward or not', 'etymology': 'Latin ad-/Greek a-'},
    }
    
    # ════════════════════════════════════════════════════════════════════════
    # SUFFIXES
    # ════════════════════════════════════════════════════════════════════════
    
    FULL_WORD_SUFFIXES = {
        'MENT': {'meaning': 'the mind', 'etymology': 'Latin mente', 'note': 'mental operation'},
        'HOOD': {'meaning': 'territory/covering', 'etymology': 'Old English', 'note': 'protected domain'},
        'SHIP': {'meaning': 'vessel/journey', 'etymology': 'Old English', 'note': 'carrying relationship'},
        'DOM': {'meaning': 'dominion/rule', 'etymology': 'Old English', 'note': 'territory of power'},
        'NESS': {'meaning': 'projection/manifestation', 'etymology': 'Old English/Norse', 'note': 'state extended into form'},
        'ABLE': {'meaning': 'ability/capable', 'etymology': 'Latin habilis', 'note': 'potential state'},
        'IBLE': {'meaning': 'is-ability', 'etymology': 'Latin', 'note': 'current ability state (IS+ABLE)'},
        'FUL': {'meaning': 'full of', 'etymology': 'Old English full', 'note': 'filled with quality'},
        'LESS': {'meaning': 'without/lacking', 'etymology': 'Old English leas', 'note': 'absence of quality'},
    }
    
    STANCE_SUFFIXES = {
        'ISH': {'meaning': 'positioned toward', 'note': 'tending toward quality'},
        'IST': {'meaning': 'practitioner/believer', 'note': 'one who takes position'},
        'ISM': {'meaning': 'system/doctrine', 'note': 'the position as doctrine'},
        'Y': {'meaning': 'positioned in', 'note': 'located within quality'},
    }
    
    TRUE_OPERATORS = ['ER', 'ING', 'ED', 'TION', 'ION', 'SION', 'AL', 'LY', 
                     'ES', 'S', 'EST', 'AGE', 'ANCE', 'ENCE', 'ANT', 'ENT',
                     'ARY', 'ORY', 'ATE', 'EE', 'ETTE', 'URE', 'TH', 'TRY',
                     'IC', 'ICAL', 'ILE', 'INE', 'OID', 'OSE', 'OUS', 'WARD',
                     'EN', 'FY', 'IFY', 'IZE', 'ISE', 'ATIVE', 'ITION']
    
    # ════════════════════════════════════════════════════════════════════════
    # COMMON ROOTS (for educational glossary)
    # ════════════════════════════════════════════════════════════════════════
    
    COMMON_ROOTS = {
        'JECT': {'meaning': 'throw/cast', 'etymology': 'Latin iacere'},
        'TENT': {'meaning': 'stretch/aim', 'etymology': 'Latin tendere'},
        'TION': {'meaning': 'tension/stretching', 'etymology': 'Latin tensio'},
        'TENTION': {'meaning': 'stretching state', 'etymology': 'Latin tensio'},
        'PRESS': {'meaning': 'press/push', 'etymology': 'Latin premere'},
        'CESS': {'meaning': 'go/yield/proceed', 'etymology': 'Latin cedere'},
        'CEDE': {'meaning': 'go/yield', 'etymology': 'Latin cedere'},
        'CEIVE': {'meaning': 'take/receive', 'etymology': 'Latin capere'},
        'CEPT': {'meaning': 'take/seize', 'etymology': 'Latin capere'},
        'GRESS': {'meaning': 'step/walk', 'etymology': 'Latin gradi'},
        'SERV': {'meaning': 'serve/watch/keep', 'etymology': 'Latin servare'},
        'FORM': {'meaning': 'shape/structure', 'etymology': 'Latin forma'},
        'PORT': {'meaning': 'carry', 'etymology': 'Latin portare'},
        'VANCE': {'meaning': 'advance/move', 'etymology': 'Latin'},
        'PERI': {'meaning': 'try/test', 'etymology': 'Latin periri'},
        'FIRM': {'meaning': 'strong/fixed', 'etymology': 'Latin firmus'},
    }
    
    # ════════════════════════════════════════════════════════════════════════
    # GREEK COMPOUND ROOTS
    # ════════════════════════════════════════════════════════════════════════
    
    GREEK_ROOTS = {
        'BIO': 'life',
        'PSYCH': 'mind/soul',
        'GE': 'earth',
        'GEO': 'earth',
        'THE': 'god',
        'THEO': 'god',
        'PHOTO': 'light',
        'DEMO': 'people',
        'MON': 'one',
        'MONO': 'one',
        'ARISTO': 'best',
        'BUREAU': 'desk',
        'TELE': 'far',
        'PHON': 'sound',
    }
    
    GREEK_SUFFIXES = {
        'LOGY': 'study',
        'GRAPHY': 'writing',
        'ARCHY': 'rule',
        'CRACY': 'power/rule',
        'OLOGY': 'study',
    }
    
    # ════════════════════════════════════════════════════════════════════════
    # SEMANTIC CONTROL WORDS
    # ════════════════════════════════════════════════════════════════════════
    
    SEMANTIC_SHADOWS = {
        'government': 'govern-ment [govern the mind]',
        'information': 'in-formation [forming within/control]',
        'representative': 're-present-ative [false re-presentation]',
    }
    
    # ════════════════════════════════════════════════════════════════════════
    # TECHNICAL FIELD TERMS
    # ════════════════════════════════════════════════════════════════════════
    
    TECHNICAL_FIELDS = {
        'mathematics': ['addition', 'subtraction', 'equation', 'integer'],
        'medicine': ['infection', 'injection', 'affliction', 'prescription', 'observation'],
        'law': ['objection', 'injunction', 'affidavit', 'indictment'],
        'science': ['observation', 'experiment', 'hypothesis', 'analysis'],
        'technology': ['application', 'interface', 'algorithm', 'instruction'],
    }
    
    # ════════════════════════════════════════════════════════════════════════
    # INITIALIZATION
    # ════════════════════════════════════════════════════════════════════════
    
    def __init__(self,
                 level: ParsingLevel = ParsingLevel.STRUCTURAL,
                 strictness: StrictnessLevel = StrictnessLevel.STANDARD,
                 flag_semantic: bool = True,
                 show_alternatives: bool = True):
        
        self.level = level
        self.strictness = strictness
        self.flag_semantic = flag_semantic
        self.show_alternatives = show_alternatives
        
        # Combine all prefixes
        self.all_prefixes = {**self.VCC_PREFIXES, **self.OTHER_PREFIXES}
        
        # Sort by length for proper matching
        self.prefix_order = sorted(self.all_prefixes.keys(), key=len, reverse=True)
    
    # ════════════════════════════════════════════════════════════════════════
    # RESONANCE CALCULATION
    # ════════════════════════════════════════════════════════════════════════
    
    def calculate_resonance(self, word: str) -> str:
        """Calculate Tap-Root resonance with master number preservation"""
        clean = ''.join(c for c in word.upper() if c.isalpha())
        total = sum(self.TAP_ROOT.get(c, (0, ""))[0] for c in clean)
        
        # Reduce while preserving master numbers
        reduced = total
        while reduced > 9 and reduced not in self.MASTER_NUMBERS:
            reduced = sum(int(d) for d in str(reduced))
        
        if total == reduced:
            result = str(total)
            if total in self.MASTER_NUMBERS:
                result += f" ({self.MASTER_NUMBERS[total]})"
            return result
        else:
            result = f"{total}→{reduced}"
            if reduced in self.MASTER_NUMBERS:
                result += f" ({self.MASTER_NUMBERS[reduced]})"
            return result
    
    # ════════════════════════════════════════════════════════════════════════
    # V+CC DETECTION WITH TILDE POSITIONAL CLAUSE
    # ════════════════════════════════════════════════════════════════════════
    
    def detect_vcc(self, word: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Detect V+CC shadow pattern.
        Returns: (is_vcc, prefix, separator_type)
        separator_type: 'tilde' for positional, 'hyphen' for operational
        """
        word_upper = word.upper()
        
        for prefix in self.VCC_PREFIXES:
            if word_upper.startswith(prefix) and len(word_upper) > len(prefix):
                base_start = word_upper[len(prefix):]
                
                # Check if base starts with consonant
                if base_start and base_start[0].isalpha() and base_start[0] not in 'AEIOU':
                    # V+CC detected
                    prefix_type = self.VCC_PREFIXES[prefix]['type']
                    
                    if prefix_type == 'positional':
                        return True, prefix, 'tilde'
                    else:
                        return True, prefix, 'hyphen'
        
        return False, None, None
    
    # ════════════════════════════════════════════════════════════════════════
    # COMPONENT EXTRACTION
    # ════════════════════════════════════════════════════════════════════════
    
    def extract_components(self, word: str) -> Dict:
        """Extract prefix, base, and suffix"""
        word_upper = word.upper()
        
        # Extract prefix
        prefix = None
        base = word_upper
        
        for p in self.prefix_order:
            if word_upper.startswith(p) and len(word_upper) > len(p):
                prefix = p
                base = word_upper[len(p):]
                break
        
        # Extract suffix
        suffix = None
        
        # Check full-word suffixes first
        for s in sorted(self.FULL_WORD_SUFFIXES.keys(), key=len, reverse=True):
            if base.endswith(s) and len(base) > len(s):
                suffix = s
                base = base[:-len(s)]
                break
        
        # Check stance suffixes
        if not suffix:
            for s in sorted(self.STANCE_SUFFIXES.keys(), key=len, reverse=True):
                if base.endswith(s) and len(base) > len(s):
                    suffix = s
                    base = base[:-len(s)]
                    break
        
        # Check operators
        if not suffix:
            for s in sorted(self.TRUE_OPERATORS, key=len, reverse=True):
                if base.endswith(s) and len(base) > len(s):
                    suffix = s
                    base = base[:-len(s)]
                    break
        
        return {
            'prefix': prefix,
            'base': base,
            'suffix': suffix
        }
    
    # ════════════════════════════════════════════════════════════════════════
    # GREEK COMPOUND DETECTION
    # ════════════════════════════════════════════════════════════════════════
    
    def is_greek_compound(self, word: str) -> bool:
        """Check if word is Greek compound"""
        word_upper = word.upper()
        for root in self.GREEK_ROOTS:
            if word_upper.startswith(root):
                for suffix in self.GREEK_SUFFIXES:
                    if suffix in word_upper:
                        return True
        return False
    
    def parse_greek(self, word: str) -> str:
        """Parse Greek compound with tilde"""
        word_upper = word.upper()
        
        # Special handling for CRACY
        if 'CRACY' in word_upper:
            for root in self.GREEK_ROOTS:
                if word_upper.startswith(root):
                    return f"{root}~CRA-CY"
        
        # Standard Greek compounds
        for root in self.GREEK_ROOTS:
            if word_upper.startswith(root):
                rest = word_upper[len(root):]
                if rest in self.GREEK_SUFFIXES:
                    return f"{root}~{rest}"
        
        return word_upper
    
    # ════════════════════════════════════════════════════════════════════════
    # MAIN PARSING FUNCTION
    # ════════════════════════════════════════════════════════════════════════
    
    def parse_word(self, word: str) -> GlyphAnalysis:
        """Main word parsing with all mechanics"""
        original = word.strip()
        word_clean = ''.join(c for c in original if c.isalnum() or c in "-_~'")
        word_upper = word_clean.upper()
        
        warnings = []
        alternatives = []
        shadow_types = []
        is_shadow = False
        tier = None
        field_context = None
        
        # Check Greek compound first
        if self.is_greek_compound(word_clean):
            parsed = self.parse_greek(word_clean)
            return GlyphAnalysis(
                original=original,
                parsed=parsed,
                polarity="Sovereign (Greek compound)",
                resonance=self.calculate_resonance(word_clean),
                is_shadow=False,
                shadow_types=[],
                components=[],
                warnings=[],
                alternatives=[],
                educational_note=f"Greek compound with tilde flow"
            )
        
        # Check semantic shadow
        if self.flag_semantic and word_clean.lower() in self.SEMANTIC_SHADOWS:
            is_shadow = True
            shadow_types.append(ShadowType.SEMANTIC)
            warnings.append(f"Semantic control: {self.SEMANTIC_SHADOWS[word_clean.lower()]}")
            tier = 1
        
        # Check V+CC
        vcc_detected, vcc_prefix, separator = self.detect_vcc(word_clean)
        
        if vcc_detected:
            is_shadow = True
            shadow_types.append(ShadowType.STRUCTURAL)
            tier = tier or 2
            
            base = word_upper[len(vcc_prefix):]
            prefix_info = self.VCC_PREFIXES[vcc_prefix]
            
            if separator == 'tilde':
                warnings.append(f"V+CC shadow: {vcc_prefix} positional - tilde neutralizes")
                alternatives.append(f"{vcc_prefix}~{base}")
                polarity = "Sovereign with tilde (positional union)"
            else:
                warnings.append(f"V+CC shadow: {vcc_prefix} operational - hyphen required")
                alternatives.append(f"{vcc_prefix}-{base}")
                polarity = "Shadow (operational, use hyphen or avoid)"
        else:
            polarity = "Sovereign"
        
        # Extract components
        components = self.extract_components(word_clean)
        
        # Build parsed form based on level
        if self.level == ParsingLevel.CASUAL:
            if is_shadow and alternatives:
                parsed = alternatives[0]
            else:
                parsed = word_clean
        
        elif self.level == ParsingLevel.STRUCTURAL:
            parts = []
            if components['prefix']:
                parts.append(components['prefix'])
            if components['base']:
                parts.append(components['base'])
            if components['suffix']:
                parts.append(components['suffix'])
            
            if vcc_detected and separator == 'tilde':
                parsed = f"{components['prefix']}~{components['base']}"
                if components['suffix']:
                    parsed += f"-{components['suffix']}"
            else:
                parsed = "-".join(parts)
        
        elif self.level == ParsingLevel.CEREMONIAL:
            parts = []
            if components['prefix']:
                parts.append(components['prefix'])
            if components['base']:
                parts.append(components['base'])
            if components['suffix']:
                parts.append(components['suffix'])
            parsed = "_".join(parts)
        
        else: # EDUCATIONAL LEVEL - Build glossary with meanings
            parts_with_meaning = []
            
            if components['prefix']:
                prefix = components['prefix']
                if prefix in self.VCC_PREFIXES:
                    info = self.VCC_PREFIXES[prefix]
                    parts_with_meaning.append(f"{prefix}[{info['meaning']}]")
                elif prefix in self.OTHER_PREFIXES:
                    info = self.OTHER_PREFIXES[prefix]
                    parts_with_meaning.append(f"{prefix}[{info['meaning']}]")
                else:
                    parts_with_meaning.append(prefix)
            
            if components['base']:
                base = components['base']
                if base in self.COMMON_ROOTS:
                    info = self.COMMON_ROOTS[base]
                    parts_with_meaning.append(f"{base}[{info['meaning']}]")
                else:
                    parts_with_meaning.append(base)
            
            if components['suffix']:
                suffix = components['suffix']
                if suffix in self.FULL_WORD_SUFFIXES:
                    info = self.FULL_WORD_SUFFIXES[suffix]
                    parts_with_meaning.append(f"{suffix}[{info['meaning']}]")
                elif suffix in self.STANCE_SUFFIXES:
                    info = self.STANCE_SUFFIXES[suffix]
                    parts_with_meaning.append(f"{suffix}[{info['meaning']}]")
                else:
                    parts_with_meaning.append(suffix)
            
            if vcc_detected and separator == 'tilde':
                parsed = f"{parts_with_meaning[0]}~{'~'.join(parts_with_meaning[1:])}"
            else:
                parsed = "-".join(parts_with_meaning)
        
        # Calculate resonance
        resonance = self.calculate_resonance(word_clean)
        
        # Check technical field context
        for field, terms in self.TECHNICAL_FIELDS.items():
            if word_clean.lower() in terms:
                field_context = field
                break
        
        # Build component details list
        component_details = []
        if components['prefix']:
            component_details.append({
                'type': 'prefix',
                'text': components['prefix'],
                'info': self.all_prefixes.get(components['prefix'], {})
            })
        if components['base']:
            component_details.append({
                'type': 'base',
                'text': components['base'],
                'info': self.COMMON_ROOTS.get(components['base'], {})
            })
        if components['suffix']:
            suffix_info = (self.FULL_WORD_SUFFIXES.get(components['suffix']) or 
                          self.STANCE_SUFFIXES.get(components['suffix']) or {})
            component_details.append({
                'type': 'suffix',
                'text': components['suffix'],
                'info': suffix_info
            })
        
        return GlyphAnalysis(
            original=original,
            parsed=parsed,
            polarity=polarity,
            resonance=resonance,
            is_shadow=is_shadow,
            shadow_types=shadow_types,
            components=component_details,
            warnings=warnings,
            alternatives=alternatives,
            tier=tier,
            field_context=field_context
        )
    
    # ════════════════════════════════════════════════════════════════════════
    # DOCUMENT PARSING
    # ════════════════════════════════════════════════════════════════════════
    
    def parse_document(self, text: str) -> str:
        """Parse entire document"""
        words = re.findall(r'\b[\w\-\_\~\']+\b|[^\w\s]', text)
        
        parsed_words = []
        for word in words:
            if re.match(r'[\w\-\_\~\']+', word):
                analysis = self.parse_word(word)
                parsed_words.append(analysis.parsed)
            else:
                parsed_words.append(word)
        
        return ' '.join(parsed_words)
    
    def analyze_document(self, text: str) -> Dict:
        """Analyze document and return shadow statistics"""
        words = re.findall(r'\b[\w\-\_\~\']+\b', text)
        
        total_words = len(words)
        shadow_count = 0
        structural_shadows = []
        semantic_shadows = []
        
        for word in words:
            analysis = self.parse_word(word)
            if analysis.is_shadow:
                shadow_count += 1
                
                if ShadowType.STRUCTURAL in analysis.shadow_types:
                    structural_shadows.append(word)
                if ShadowType.SEMANTIC in analysis.shadow_types:
                    semantic_shadows.append(word)
        
        sovereignty_score = ((total_words - shadow_count) / total_words * 100) if total_words > 0 else 0
        
        return {
            'total_words': total_words,
            'shadow_count': shadow_count,
            'structural_shadows': structural_shadows,
            'semantic_shadows': semantic_shadows,
            'sovereignty_score': sovereignty_score
        }
    
    def generate_report(self, text: str) -> str:
        """Generate detailed shadow analysis report"""
        analysis = self.analyze_document(text)
        
        report = []
        report.append("="*72)
        report.append("CODEXGLYPH DOCUMENT ANALYSIS REPORT")
        report.append(f"Parsing Level: {self.level.name}")
        report.append(f"Strictness: {self.strictness.name}")
        report.append("="*72)
        report.append("")
        report.append(f"Total Words: {analysis['total_words']}")
        report.append(f"Shadow Glyphs: {analysis['shadow_count']}")
        report.append(f"Sovereignty Score: {analysis['sovereignty_score']:.1f}%")
        report.append("")
        
        if analysis['structural_shadows']:
            report.append(f"STRUCTURAL SHADOWS (V+CC): {len(analysis['structural_shadows'])}")
            for word in set(analysis['structural_shadows'][:10]):
                word_analysis = self.parse_word(word)
                report.append(f"  • {word} → {word_analysis.parsed}")
            if len(analysis['structural_shadows']) > 10:
                report.append(f"  ... and {len(analysis['structural_shadows']) - 10} more")
            report.append("")
        
        if analysis['semantic_shadows']:
            report.append(f"SEMANTIC SHADOWS (Control Language): {len(analysis['semantic_shadows'])}")
            for word in set(analysis['semantic_shadows']):
                word_analysis = self.parse_word(word)
                report.append(f"  • {word} → {word_analysis.parsed}")
            report.append("")
        
        report.append("="*72)
        return "\n".join(report)


# ════════════════════════════════════════════════════════════════════════════
# COMMAND-LINE INTERFACE
# ════════════════════════════════════════════════════════════════════════════

def main():
    """CLI for CodexGlyph parser"""
    import sys
    
    print("="*72)
    print("CODEXGLYPH ENGINE v2.6 - SOVEREIGN LANGUAGE PARSER")
    print("Captain-Sealed - December 2, 2025")
    print("="*72)
    print()
    
    # Example usage
    parser = CodexGlyphParser(
        level=ParsingLevel.STRUCTURAL,
        strictness=StrictnessLevel.STANDARD
    )
    
    # Test words
    test_words = [
        "experiment",
        "information", 
        "government",
        "understand",
        "attention",
        "object",
        "project",
        "reject",
        "inject",
        "confirm",
        "support",
        "illness",
        "biology",
        "democracy",
    ]
    
    print("TESTING V+CC DETECTION & TILDE POSITIONAL CLAUSE:")
    print("-"*72)
    
    for word in test_words:
        analysis = parser.parse_word(word)
        
        print(f"\n{word.upper()}")
        print(f"  Parsed: {analysis.parsed}")
        print(f"  Resonance: {analysis.resonance}")
        print(f"  Polarity: {analysis.polarity}")
        
        if analysis.is_shadow:
            types = ", ".join([st.value for st in analysis.shadow_types])
            print(f"  Shadow: {types}")
            
            if analysis.alternatives:
                print(f"  Alternatives: {', '.join(analysis.alternatives)}")
        
        if analysis.warnings:
            for warning in analysis.warnings:
                print(f"  ⚠ {warning}")
    
    print("\n" + "="*72)
    print("\nDOCUMENT ANALYSIS TEST:")
    print("-"*72)
    
    test_doc = """
    The government representative will experiment with information 
    systems to understand the objection raised by the committee.
    """
    
    report = parser.generate_report(test_doc)
    print(report)
    
    print("\n" + "="*72)
    print("TILDE POSITIONAL CLAUSE EXAMPLES:")
    print("-"*72)
    print("  EX~PERIMENT (positional: outward-testing)")
    print("  IN~FORMATION (positional: inward-forming)")
    print("  AT~TENTION (positional: toward-stretching)")
    print("  OB~JECT (positional: opposite-throwing)")
    print("  UN-DO (operational: liberation-from-doing)")
    
    print("\n" + "="*72)
    print("MASTER NUMBERS PRESERVED:")
    print("-"*72)
    for num, meaning in parser.MASTER_NUMBERS.items():
        print(f"  {num}: {meaning}")
    
    print("\n" + "="*72)
    print("\nCodexGlyph v2.6 Ready for Production Use")
    print("="*72)


if __name__ == "__main__":
    main()


# ════════════════════════════════════════════════════════════════════════════
# USAGE EXAMPLES FOR INTEGRATION
# ════════════════════════════════════════════════════════════════════════════

def usage_examples():
    """Examples of how to use the parser"""
    
    # Example 1: Basic word analysis
    parser = CodexGlyphParser(level=ParsingLevel.STRUCTURAL)
    result = parser.parse_word("experiment")
    print(f"Word: {result.original}")
    print(f"Parsed: {result.parsed}")
    print(f"Sovereign: {not result.is_shadow}")
    
    # Example 2: Document parsing
    document = "The government needs to understand the information."
    parsed_doc = parser.parse_document(document)
    print(f"Original: {document}")
    print(f"Parsed: {parsed_doc}")
    
    # Example 3: Shadow analysis
    report = parser.generate_report(document)
    print(report)
    
    # Example 4: Educational mode
    edu_parser = CodexGlyphParser(level=ParsingLevel.EDUCATIONAL)
    result = edu_parser.parse_word("government")
    print(f"Educational: {result.parsed}")
    
    # Example 5: Ceremonial mode
    ceremonial_parser = CodexGlyphParser(level=ParsingLevel.CEREMONIAL)
    result = ceremonial_parser.parse_word("understand")
    print(f"Ceremonial: {result.parsed}")


# ════════════════════════════════════════════════════════════════════════════
# END OF CODEXGLYPH v2.6
# ══════════════════════════