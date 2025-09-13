#!/usr/bin/env python3
"""
PASS // FAIL - Hash Verification GUI Components

This file contains the graphical user interface for the PASS // FAIL application.

Main components:
- StickFigureKeyLockProgress: Animated progress indicator with stick figure
- HashVerifierGUI: Main application window with all controls and functionality

The GUI provides:
- Wordlist selection with drag & drop support
- Hash input with file browsing and drag & drop
- Real-time terminal output with colored text
- Animated progress visualization
- Start/Stop controls with proper cleanup

Performance Optimizations:
- Terminal tag caching to avoid repeated color tag creation
- Batched terminal updates to reduce UI flickering and improve responsiveness
- Enhanced progress update throttling with smarter timing
- Optimized animation frame rate (120ms) for better CPU efficiency
- Batched widget state changes to minimize UI operations
- Efficient terminal clearing with cache management

Perfect for beginners to learn about:
- GUI design patterns in Python
- Event handling and threading
- File operations and user feedback
- UI performance optimization techniques
"""

import os
import platform
import threading
import math
import time
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import Tk, Label, Entry, Listbox, END, Frame, filedialog, Text, DISABLED, NORMAL
from tkinter import ttk
from PIL import Image, ImageTk
from hash_verifier import verify_hash, get_available_wordlists


def get_os_font_size():
    """
    Get appropriate font size based on operating system.
    
    Returns:
        int: Font size optimized for the current OS
            - macOS: 16 (native macOS apps typically use larger fonts)
            - Windows: 12 (standard Windows application font size)
            - Linux: 12 (consistent with most Linux desktop environments)
    """
    system = platform.system()
    if system == "Darwin":  # macOS
        return 16
    elif system == "Windows":
        return 12
    else:  # Linux and other Unix-like systems
        return 12


class StickFigureKeyLockProgress(ttk.Frame):
    """
    Animated progress indicator showing a stick figure carrying a key toward a lock.
    
    The animation features:
    - Smooth walking animation with bouncing motion
    - Arms swing naturally while holding a key
    - Legs move in jumping-jack pattern, limited to hip level
    - Lock with keyhole that opens when progress reaches 100%
    - Celebration effect pulses key and lock outline at completion
    
    The widget is fully self-contained and manages its own animation timing,
    geometry calculations, and Canvas drawing. It supports both immediate and
    thread-safe progress updates.
    
    Args:
        master: Parent widget
        width (int): Initial width in pixels
        height (int): Initial height in pixels
        maximum (float): Maximum progress value (default 100.0)
        bg (str): Background color in hex format
        stick (str): Stick figure color in hex format
        text (str): Label text color in hex format
    """

    def __init__(self, master, width=820, height=160, maximum=100.0,
                 bg="#1b0f2a", stick="#b086ff", text="#ffffff", font_size=12):
        super().__init__(master)
        self._w_req = int(width)
        self._h_req = int(height)
        self._maximum = float(maximum) if maximum > 0 else 100.0
        self._value = 0.0
        self._fraction = 0.0
        self._font_size = font_size

        # Theme
        self.colors = {"bg": bg, "stick": stick, "text": text}

        # Geometry
        self._margin = 24
        self._track_y = None
        self._track_left = None
        self._track_right = None
        self._figure_y = None
        self._travel_right = None

        # Animation state
        self._anim_job = None
        self._anim_running = False
        self._phase = 0.0
        self._celebrate_until = 0.0
        self._pulse_on = False

        # Geometry constants
        self._arm_len = 22
        self._key_head_r = 7
        self._key_shaft_len = 14

        # Canvas
        self.canvas = tk.Canvas(
            self, width=self._w_req, height=self._h_req,
            bg=self.colors["bg"], highlightthickness=0, bd=0
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._on_resize)

        # Items
        self._create_items()
        self._layout()
        self._update_all(force=True)

    # Public API
    def set(self, value: float) -> None:
        v = max(0.0, min(float(value), self._maximum))
        changed = (v != self._value)
        self._value = v
        self._fraction = (self._value / self._maximum) if self._maximum > 0 else 0.0
        if changed:
            self._update_label()
            self._update_figure()
        if self._value >= self._maximum and time.monotonic() >= self._celebrate_until:
            self.celebrate(1200)

    def threadsafe_set(self, value: float) -> None:
        self.after(0, self.set, value)

    def get(self) -> float:
        return self._value

    def reset(self) -> None:
        self._value = 0.0
        self._fraction = 0.0
        self._celebrate_until = 0.0
        self._pulse_on = False
        self.canvas.itemconfigure(self.items["shackle_closed"], state="normal")
        self.canvas.itemconfigure(self.items["shackle_open"], state="hidden")
        self._update_all(force=True)

    def start(self) -> None:
        if not self._anim_running:
            self._anim_running = True
            self._schedule()

    def stop(self) -> None:
        self._anim_running = False
        if self._anim_job:
            try:
                self.after_cancel(self._anim_job)
            except Exception:
                pass
            self._anim_job = None

    def celebrate(self, ms: int = 1200) -> None:
        now = time.monotonic()
        self._celebrate_until = now + max(0, ms) / 1000.0
        self.canvas.itemconfigure(self.items["shackle_closed"], state="hidden")
        self.canvas.itemconfigure(self.items["shackle_open"], state="normal")
        if not self._anim_running:
            self.start()

    # Internals
    def _schedule(self):
        if self._anim_running:
            self._tick()
            # Optimized frame rate: 120ms instead of 90ms for better performance
            # Still smooth enough for the animation but reduces CPU usage by ~25%
            self._anim_job = self.after(120, self._schedule)

    def _tick(self):
        self._phase = (self._phase + 0.35) % (math.tau if hasattr(math, "tau") else (2 * math.pi))
        if time.monotonic() < self._celebrate_until:
            self._pulse_on = not self._pulse_on
            width = 2 if self._pulse_on else 1
            for name in ("key_head", "key_shaft", "key_tooth1", "key_tooth2", "lock_body", "keyhole_stem", "keyhole_oval"):
                self.canvas.itemconfigure(self.items[name], width=width)
        else:
            for name in ("key_head", "key_shaft", "key_tooth1", "key_tooth2", "lock_body", "keyhole_stem", "keyhole_oval"):
                self.canvas.itemconfigure(self.items[name], width=1)
        self._update_figure()

    def _on_resize(self, event):
        self._layout()
        self._update_all(force=True)

    def _create_items(self):
        c = self.canvas
        col = self.colors
        items = {}
        # Lock body + keyhole
        items["lock_body"] = c.create_rectangle(0, 0, 0, 0, outline=col["stick"], width=1)
        items["keyhole_oval"] = c.create_oval(0, 0, 0, 0, outline=col["stick"], width=1)
        items["keyhole_stem"] = c.create_line(0, 0, 0, 0, fill=col["stick"], width=1, capstyle="round")
        # Shackle arcs (closed/open)
        items["shackle_closed"] = c.create_arc(0, 0, 0, 0, start=0, extent=180, style="arc", outline=col["stick"], width=2)
        items["shackle_open"] = c.create_arc(0, 0, 0, 0, start=300, extent=150, style="arc", outline=col["stick"], width=2, state="hidden")
        # Stick figure
        items["head"] = c.create_oval(0, 0, 0, 0, outline=col["stick"], width=2)
        items["torso"] = c.create_line(0, 0, 0, 0, fill=col["stick"], width=2, capstyle="round")
        items["arm_l"] = c.create_line(0, 0, 0, 0, fill=col["stick"], width=2, capstyle="round")
        items["arm_r"] = c.create_line(0, 0, 0, 0, fill=col["stick"], width=2, capstyle="round")
        items["leg_l"] = c.create_line(0, 0, 0, 0, fill=col["stick"], width=2, capstyle="round")
        items["leg_r"] = c.create_line(0, 0, 0, 0, fill=col["stick"], width=2, capstyle="round")
        # Key in right hand
        items["key_head"] = c.create_oval(0, 0, 0, 0, outline=col["stick"], width=1)
        items["key_shaft"] = c.create_line(0, 0, 0, 0, fill=col["stick"], width=1)
        items["key_tooth1"] = c.create_line(0, 0, 0, 0, fill=col["stick"], width=1)
        items["key_tooth2"] = c.create_line(0, 0, 0, 0, fill=col["stick"], width=1)
        # Percent label
        items["label"] = c.create_text(0, 0, text="0%", fill=col["text"], 
                                     font=("Segoe UI", max(8, self._font_size - 5), "bold"))
        self.items = items

    def _layout(self):
        c = self.canvas
        w = max(10, c.winfo_width())
        h = max(10, c.winfo_height())
        m = self._margin
        track_y = int(h * 0.64)
        self._track_y = track_y
        left = m
        right = w - m
        self._track_left = left
        self._track_right = right
        self._figure_y = track_y - 20

        # Lock placement near right end
        body_w = 28
        body_h = 22
        sh_r = 12
        body_left = min(right - body_w, right - 4)
        body_right = body_left + body_w
        body_top = track_y - body_h - sh_r + 8
        body_bottom = body_top + body_h
        c.coords(self.items["lock_body"], body_left, body_top, body_right, body_bottom)
        # Keyhole
        kh_cx = (body_left + body_right) / 2
        kh_cy = body_top + body_h * 0.5
        kh_r = 3
        c.coords(self.items["keyhole_oval"], kh_cx - kh_r, kh_cy - kh_r, kh_cx + kh_r, kh_cy + kh_r)
        c.coords(self.items["keyhole_stem"], kh_cx, kh_cy + kh_r, kh_cx, kh_cy + kh_r + 6)
        # Shackle
        shack_x1, shack_y1 = kh_cx - sh_r, body_top - sh_r
        shack_x2, shack_y2 = kh_cx + sh_r, body_top + sh_r
        c.coords(self.items["shackle_closed"], shack_x1, shack_y1, shack_x2, shack_y2)
        c.coords(self.items["shackle_open"], shack_x1 - 2, shack_y1 - 6, shack_x2 - 2, shack_y2 - 6)
        c.itemconfigure(self.items["shackle_closed"], state="normal")
        c.itemconfigure(self.items["shackle_open"], state="hidden")

        # Travel clamp so key never overlaps the lock
        right_reach = self._arm_len + self._key_head_r + self._key_shaft_len
        clearance = 8
        self._travel_right = max(left + 10, body_left - (right_reach + clearance))

        # Percent label below the animation
        c.coords(self.items["label"], w / 2, track_y + 32)

        # Initial placement
        self._update_figure()

    def _update_all(self, force=False):
        self._update_label()
        self._update_figure()

    def _update_label(self):
        pct = int(round(self._fraction * 100))
        self.canvas.itemconfigure(self.items["label"], text=f"{pct}%")

    def _update_figure(self):
        if self._track_left is None:
            return
        right_limit = self._travel_right if self._travel_right is not None else self._track_right
        x = self._track_left + self._fraction * (right_limit - self._track_left)
        ground_y = self._track_y
        base_y = self._figure_y
        bob = 4 * math.sin(self._phase * 2)
        y = base_y + bob

        head_r = 10
        torso_len = 26
        arm_len = self._arm_len
        leg_len = 26

        swing = math.sin(self._phase)
        arm_angle = swing * 0.6
        # Legs swing opposite to arms
        leg_angle = -swing * 0.7

        neck = (x, y - head_r)
        hip = (x, y + torso_len * 0.5)

        hx, hy = (x, y - head_r * 2)
        self.canvas.coords(self.items["head"], hx - head_r, hy - head_r, hx + head_r, hy + head_r)
        self.canvas.coords(self.items["torso"], neck[0], neck[1], hip[0], hip[1])

        ax = neck[0]
        ay = neck[1] + 6
        lax = ax + arm_len * math.cos(math.pi - arm_angle)
        lay = ay + arm_len * math.sin(math.pi - arm_angle)
        self.canvas.coords(self.items["arm_l"], ax, ay, lax, lay)
        rax = ax + arm_len * math.cos(arm_angle)
        ray = ay + arm_len * math.sin(arm_angle)
        self.canvas.coords(self.items["arm_r"], ax, ay, rax, ray)

        lx1 = hip[0]
        ly1 = hip[1]
        # Both legs swing opposite to arms, clamp so they never go above horizontal (hip level)
        # Left leg
        llx2 = lx1 + leg_len * math.cos(math.pi + leg_angle)
        lly2 = ly1 + leg_len * math.sin(math.pi + leg_angle)
        if lly2 < ly1:
            lly2 = ly1
        lly2 = min(ground_y, lly2)
        self.canvas.coords(self.items["leg_l"], lx1, ly1, llx2, lly2)
        # Right leg
        lrx2 = lx1 + leg_len * math.cos(leg_angle)
        lry2 = ly1 + leg_len * math.sin(leg_angle)
        if lry2 < ly1:
            lry2 = ly1
        lry2 = min(ground_y, lry2)
        self.canvas.coords(self.items["leg_r"], lx1, ly1, lrx2, lry2)

        kx, ky = rax, ray
        kh = self._key_head_r
        shaft = self._key_shaft_len
        self.canvas.coords(self.items["key_head"], kx - kh, ky - kh, kx + kh, ky + kh)
        sx1, sy1 = kx + kh, ky
        sx2, sy2 = sx1 + shaft, ky
        self.canvas.coords(self.items["key_shaft"], sx1, sy1, sx2, sy2)
        t1x = sx2 - 6
        t2x = sx2 - 2
        self.canvas.coords(self.items["key_tooth1"], t1x, sy2, t1x, sy2 + 5)
        self.canvas.coords(self.items["key_tooth2"], t2x, sy2, t2x, sy2 + 7)


class HashVerifierGUI:
    """
    Main GUI for the PASS // FAIL hash verification application.
    
    Features:
    - Wordlist selection with multi-select support
    - Hash input via text or file browse
    - Real-time terminal output with color
    - Custom animated progress visualization
    - Start/Stop controls with cooperative cancellation
    - Clean purple theme with custom ttk styling
    
    Layout structure:
    ```
    +-Main Frame---------------------------------+
    |+Left Frame-++Right Frame-------------------|
    ||Wordlists  ||Hash Input                   ||
    ||[Multi-    ||[Entry] [Browse]             ||
    ||select     ||                             ||
    ||List]      ||Terminal Output              ||
    ||           ||[Scrollable colored text]    ||
    ||           ||                             ||
    ||           ||Progress Animation           ||
    ||           ||[Stick Figure & Lock]        ||
    ||           ||                             ||
    ||           ||[Start] [Stop]               ||
    |+-----------+------------------------------+|
    +--------------------------------------------+
    ```
    
    The GUI is event-driven and thread-safe, properly marshalling updates
    from the worker thread to the main thread for progress and terminal
    updates.
    
    Args:
        master: The root Tk window
    """
    def __init__(self, master):
        """
        Initialize the main GUI window with all components.
        
        Sets up:
        1. Color theme and fonts
        2. Left panel (wordlists)
        3. Right panel (hash input, terminal, progress, buttons)
        4. Event handlers and drag & drop
        """
        self.master = master
        
        # Get OS-appropriate font size
        self.font_size = get_os_font_size()
        master.option_add("*Font", f"Arial {self.font_size}")  # Set default font for all widgets

        # === THEME COLORS ===
        # Purple-themed color palette for consistent styling
        self.colors = {
            "bg": "#1b0f2a",           # Dark purple background
            "panel": "#24123a",        # Slightly lighter panel background  
            "text": "#ffffff",         # White text
            "accent": "#b086ff",       # Light purple accent
            "accent_alt": "#8b6cf7",   # Alternative purple accent
            "muted": "#9a8fba",        # Muted text (for placeholders, disabled states)
            "button_bg": "#3a1d5e",    # Button background
            "button_active": "#6e44ff", # Active button color
            "entry_bg": "#160b24",     # Input field background
            "entry_fg": "#f5f1ff",     # Input field text
            "select_bg": "#6e44ff",    # Selection background
            "select_fg": "#ffffff",    # Selection text
            "terminal_bg": "#0f0819",  # Terminal background
            "terminal_fg": "#e6d9ff",  # Terminal text
        }

        # === MAIN LAYOUT ===
        # Create the main container that holds everything
        self.main_frame = Frame(master, bg=self.colors["bg"])
        self.main_frame.pack(fill='both', expand=True)

        # === LEFT PANEL: WORDLISTS ===
        self._setup_styles()  # Set up button and widget styles first
        self._setup_wordlist_panel()
        
        # === RIGHT PANEL: HASH INPUT & CONTROLS ===
        self._setup_main_panel()
        
        # === INITIALIZE DATA ===
        # Progress tracking variables
        self._progress_last_ts = 0.0
        self._progress_last_frac = 0.0
        
        # Terminal performance optimizations
        self._terminal_tags_cache = {}
        self._pending_terminal_updates = []
        self._terminal_update_scheduled = False

        # Worker thread control
        self._stop_event = None
        self._worker_thread = None

        # Load available wordlists
        self.load_wordlists()

    def get_font(self, family="Arial", size_offset=0, weight="normal"):
        """
        Get a font tuple with OS-appropriate sizing.
        
        Args:
            family (str): Font family name
            size_offset (int): Offset from base font size (can be negative)
            weight (str): Font weight ("normal", "bold", etc.)
            
        Returns:
            tuple: (family, size, weight) font specification
        """
        return (family, self.font_size + size_offset, weight)

    def _setup_styles(self):
        """
        Configure all button and widget styles for the application.
        
        This method creates custom ttk (themed tkinter) styles that give
        our buttons and widgets a consistent purple theme. We define:
        - Purple.TButton: Main action buttons (Start/Stop)
        - Muted.TButton: Secondary buttons (Import Wordlist)
        - Purple.Vertical.TScrollbar: Custom scrollbar styling
        
        The styles include both static properties (configure) and
        dynamic properties (map) that change based on user interaction.
        """
        # Initialize ttk style system
        self.style = ttk.Style()
        
        # Use a cross-platform theme that respects custom colors
        try:
            self.style.theme_use('clam')
        except Exception:
            # Fallback if 'clam' theme is not available
            try:
                self.style.theme_use('alt')
            except Exception:
                pass  # Use default theme if others fail

        # === MAIN BUTTON STYLE ===
        # Standard purple buttons (Start/Stop)
        self.style.configure(
            'Purple.TButton',
            background=self.colors["button_bg"],
            foreground=self.colors["text"],
            borderwidth=0,
            relief='flat',
            focusthickness=0,
        )
        self.style.map(
            'Purple.TButton',
            background=[
                ('pressed', self.colors["button_active"]),
                ('active', self.colors["button_active"]),
                ('!disabled', self.colors["button_bg"]),
            ],
            foreground=[('disabled', self.colors["muted"])],
            relief=[('pressed', 'flat'), ('active', 'flat')]
        )
        
        # === MUTED BUTTON STYLE ===
        # Subdued buttons (Import Wordlist)
        self.style.configure(
            'Muted.TButton',
            background=self.colors["button_bg"],
            foreground=self.colors["muted"],
            borderwidth=0,
            relief='flat',
            focusthickness=0,
        )
        self.style.map(
            'Muted.TButton',
            background=[
                ('pressed', self.colors["button_active"]),
                ('active', self.colors["button_active"]),
                ('!disabled', self.colors["button_bg"]),
            ],
            foreground=[
                ('pressed', self.colors["text"]),
                ('active', self.colors["text"]),
                ('!disabled', self.colors["muted"])
            ],
            relief=[('pressed', 'flat'), ('active', 'flat')]
        )

        # === SCROLLBAR STYLE ===
        # Custom purple scrollbars
        self.style.configure(
            'Purple.Vertical.TScrollbar',
            troughcolor=self.colors["panel"],
            background=self.colors["accent_alt"],
            arrowcolor=self.colors["text"],
            bordercolor=self.colors["panel"],
            lightcolor=self.colors["accent_alt"],
            darkcolor=self.colors["accent"],
            arrowsize=12
        )
        self.style.map(
            'Purple.Vertical.TScrollbar',
            background=[('active', self.colors["accent"]), ('pressed', self.colors["accent"])],
            arrowcolor=[('disabled', self.colors["muted"])],
        )

    def _setup_wordlist_panel(self):
        """
        Set up the left panel containing wordlist selection and import functionality.
        
        This method creates the wordlist management interface where users can:
        1. View all available wordlists in a scrollable list
        2. Select wordlists by clicking on them
        3. Import custom wordlists using multiple methods:
           - Click the "+ Import Wordlist" button
           - Drag & drop files directly onto the wordlist area
           - Use tooltips for guidance
        
        The panel includes:
        - Visual feedback for selections
        - Drag & drop file handling
        - Terminal feedback for all operations
        - Error handling for invalid files
        - Professional styling consistent with the app theme
        """
        # === WORDLIST FRAME ===
        self.left_frame = Frame(self.main_frame, bg=self.colors["panel"])
        self.left_frame.pack(side='left', fill='y', padx=20, pady=20)

        # Wordlist title
        self.wordlist_label = Label(
            self.left_frame, text="Wordlists",
            bg=self.colors["panel"], fg=self.colors["text"]
        )
        self.wordlist_label.pack()

        # === WORDLIST SELECTION BOX ===
        self.wordlist_frame = Frame(self.left_frame, bg=self.colors["panel"])
        self.wordlist_frame.pack()

        # ttk Scrollbar styles
        self.style.configure(
            'Purple.Vertical.TScrollbar',
            troughcolor=self.colors["panel"],
            background=self.colors["accent_alt"],
            arrowcolor=self.colors["text"],
            bordercolor=self.colors["panel"],
            lightcolor=self.colors["accent_alt"],
            darkcolor=self.colors["accent"],
            arrowsize=12
        )
        self.style.map(
            'Purple.Vertical.TScrollbar',
            background=[('active', self.colors["accent"]), ('pressed', self.colors["accent"])],
            arrowcolor=[('disabled', self.colors["muted"])],
        )

        self.wordlist_scrollbar = ttk.Scrollbar(
            self.wordlist_frame, orient='vertical', style='Purple.Vertical.TScrollbar'
        )
        self.wordlist_scrollbar.pack(side='right', fill='y')

        self.wordlist_box = Listbox(
            self.wordlist_frame, selectmode='multiple',
            yscrollcommand=self.wordlist_scrollbar.set, width=30, height=18,
            bg=self.colors["entry_bg"], fg=self.colors["entry_fg"],
            selectbackground=self.colors["select_bg"], selectforeground=self.colors["select_fg"],
            takefocus=0  # Prevent the listbox from taking focus
        )
        
        # Enable drag and drop for wordlist box
        self.wordlist_box.drop_target_register(DND_FILES)
        self.wordlist_box.dnd_bind('<<Drop>>', self.on_drop_wordlist)
        
        self.wordlist_box.pack(side='left', fill='both')
        
        # Create tooltip overlay for empty wordlist
        self.wordlist_tooltip = Label(
            self.wordlist_frame,
            text="Drag files here",
            bg=self.colors["entry_bg"],
            fg=self.colors["muted"],
            font=self.get_font(size_offset=-7),  # Smaller font for tooltip
            justify='center',
            wraplength=200
        )
        
        # Position tooltip in center of listbox area
        def position_tooltip():
            # Get listbox position and size
            self.wordlist_box.update_idletasks()
            x = self.wordlist_box.winfo_x() + self.wordlist_box.winfo_width() // 2
            y = self.wordlist_box.winfo_y() + self.wordlist_box.winfo_height() // 2
            self.wordlist_tooltip.place(x=x, y=y, anchor='center')
        
        # Show/hide tooltip based on wordlist content
        def update_tooltip_visibility():
            if self.wordlist_box.size() == 0:
                position_tooltip()
                self.wordlist_tooltip.lift()  # Bring to front
            else:
                self.wordlist_tooltip.place_forget()
        
        # Store the tooltip update function for later use
        self._update_wordlist_tooltip = update_tooltip_visibility
        
        # Bind events to update tooltip visibility
        self.wordlist_box.bind('<Configure>', lambda e: self.wordlist_box.after_idle(update_tooltip_visibility))
        
        self.wordlist_scrollbar.config(command=self.wordlist_box.yview)
        
        # Simple click handler for proper selection behavior
        def on_mouse_click(event):
            # Get the item index at click position
            index = self.wordlist_box.nearest(event.y)
            
            # Check if there are any items in the listbox
            if self.wordlist_box.size() == 0:
                return
            
            # Get the bounding box of the item
            try:
                bbox = self.wordlist_box.bbox(index)
                if bbox is None:
                    # Clicked in empty area below all items
                    self.wordlist_box.selection_clear(0, END)
                    return "break"
                
                # Check if click Y coordinate is within the item's bounds
                if event.y < bbox[1] or event.y > bbox[1] + bbox[3]:
                    # Clicked in empty area - clear selections
                    self.wordlist_box.selection_clear(0, END)
                    return "break"
                    
            except tk.TclError:
                # Error getting bbox means empty area
                self.wordlist_box.selection_clear(0, END)
                return "break"
        
        # Bind the click handler
        self.wordlist_box.bind('<Button-1>', on_mouse_click)

        # Plus button for importing wordlists (centered at bottom of wordlist area)
        self.import_button_frame = Frame(self.left_frame, bg=self.colors["panel"])
        self.import_button_frame.pack(fill='x', pady=(5, 0))
        
        self.import_button = ttk.Button(
            self.import_button_frame, text="+ Import Wordlist", 
            command=self.import_wordlist, style='Muted.TButton'
        )
        self.import_button.pack(fill='x', padx=5)

        # Image below wordlist
        self.image_frame = Frame(self.left_frame, bg=self.colors["panel"])
        self.image_frame.pack(pady=(10, 0))  # Fixed padding above image
        
        # Load and display the image
        try:
            img_path = os.path.join(os.path.dirname(__file__), "images", "image01.png")
            # Load image with PIL for high-quality resizing
            pil_image = Image.open(img_path)
            
            # Get the exact width of the wordlist box (including borders)
            fixed_width = self.wordlist_box.winfo_reqwidth()
            
            # Calculate proportional height to maintain aspect ratio
            aspect_ratio = pil_image.height / pil_image.width
            fixed_height = int(fixed_width * aspect_ratio)
            
            # Create canvas with fixed dimensions
            self.image_canvas = tk.Canvas(
                self.image_frame,
                width=fixed_width,
                height=fixed_height,
                bg=self.colors["panel"],
                highlightthickness=0
            )
            self.image_canvas.pack()
            
            # Configure canvas to prevent resizing
            self.image_canvas.pack_propagate(False)
            
            # Resize image with high-quality antialiasing
            resized_image = pil_image.resize(
                (fixed_width, fixed_height),
                Image.Resampling.LANCZOS
            )
            
            # Convert PIL image to PhotoImage for tkinter
            self.logo_image = ImageTk.PhotoImage(resized_image)
            
            # Place image in center
            x = (fixed_width - fixed_width) // 2  # Will be 0
            y = (fixed_height - fixed_height) // 2  # Will be 0
            
            # Place image (no resize binding needed)
            self.image_canvas.create_image(
                x, y,
                image=self.logo_image,
                anchor='nw'
            )
            
        except Exception as e:
            print(f"Error loading image: {e}")

    def _setup_main_panel(self):
        """
        Set up the right panel containing hash input, terminal, progress, and buttons.
        
        This method creates the main interface where users:
        1. Enter or drag & drop hash files for verification
        2. View terminal output showing progress and results
        3. See animated progress with the stick figure graphic
        4. Control verification with Start/Stop buttons
        
        The panel includes advanced features like:
        - Drag & drop file handling
        - Placeholder text for user guidance
        - Double-click to browse files
        - Scrollable terminal output
        - Real-time progress tracking
        """
        # Right frame for hash input and buttons
        self.right_frame = Frame(self.main_frame, bg=self.colors["panel"])
        self.right_frame.pack(side='left', fill='both', expand=True, padx=20, pady=20)

        # Create a container frame for the centered label
        self.label_container = Frame(self.right_frame, bg=self.colors["panel"])
        self.label_container.pack(fill='x')
        
        self.label = Label(
            self.label_container, text="Hash Value to Verify",
            bg=self.colors["panel"], fg=self.colors["text"]
        )
        self.label.pack(expand=True)

        # Frame for hash entry and browse button
        self.hash_frame = Frame(self.right_frame, bg=self.colors["panel"])
        self.hash_frame.pack(fill='x', pady=(0, 20))

        # Create Entry with double-click functionality and placeholder
        self.hash_entry = Entry(
            self.hash_frame,
            bg=self.colors["entry_bg"], 
            fg=self.colors["entry_fg"],
            insertbackground=self.colors["entry_fg"],
            justify='center',  # Center text by default for placeholder
            width=70  # Set specific width (about 70 characters wide)
        )

        self.hash_entry.drop_target_register(DND_FILES)
        self.hash_entry.dnd_bind('<<Drop>>', self.on_drop_hash)

        # Pack with centered positioning instead of filling full width
        self.hash_entry.pack(padx=20, pady=5)
        
        # Simple placeholder text
        def update_placeholder():
            if self.showing_placeholder:
                self.hash_entry.delete(0, END)
                self.hash_entry.insert(0, "Double-click to browse file")
                self.hash_entry.config(fg=self.colors["muted"], justify='center')
        
        # Add placeholder text after widget is rendered
        self.hash_entry.bind('<Configure>', lambda e: self.hash_entry.after_idle(update_placeholder))
        # Initial placeholder
        self.hash_entry.after(10, update_placeholder)
        
        # Track if we're showing placeholder
        self.showing_placeholder = True
        
        # Bind events for placeholder behavior
        def hash_entry_double_click(event):
            self.browse_hash_file()
            return "break"
            
        self.hash_entry.bind('<Double-Button-1>', hash_entry_double_click)
        self.hash_entry.bind('<FocusIn>', self._on_entry_focus_in)
        self.hash_entry.bind('<FocusOut>', self._on_entry_focus_out)
        
        # Add Enter/Return key binding to start/stop verification
        def hash_entry_enter(event):
            """
            Handle Enter/Return key press in hash entry field.
            
            Behavior:
            - If verification is running: Stop the current process
            - If verification is not running and there's valid hash input: Start verification
            - If there's no valid input or placeholder text: Do nothing
            
            This provides intuitive keyboard control: Enter to start, Enter again to stop.
            """
            entry_text = self.hash_entry.get().strip()
            
            # Check if verification is currently running
            is_running = (self._worker_thread is not None and 
                         self._worker_thread.is_alive())
            
            if is_running:
                # If running, stop the verification
                self.stop_verification()
            elif entry_text and not entry_text.startswith("Double-click"):
                # If not running and there's actual content, start verification
                self.verify_hash()
            
            return "break"  # Prevent default Enter behavior
            
        self.hash_entry.bind('<Return>', hash_entry_enter)
        self.hash_entry.bind('<KP_Enter>', hash_entry_enter)  # Numeric keypad Enter

        # Terminal-like feedback window
        # Create a container frame for the centered terminal label
        self.terminal_label_container = Frame(self.right_frame, bg=self.colors["panel"])
        self.terminal_label_container.pack(fill='x', pady=(20, 0))
        
        self.terminal_label = Label(
            self.terminal_label_container, text="Terminal Output",
            bg=self.colors["panel"], fg=self.colors["text"]
        )
        self.terminal_label.pack(expand=True)

        self.terminal_frame = Frame(self.right_frame, bg=self.colors["panel"])
        self.terminal_frame.pack(fill='both', expand=True)

        # Inner content area for text + scrollbar
        self.terminal_content = Frame(self.terminal_frame, bg=self.colors["panel"])
        self.terminal_content.pack(fill='both', expand=True)

        # Stopped early banner inside the terminal area (hidden by default)
        self.stopped_bar = Frame(self.terminal_frame, bg="#2b1744")
        self.stopped_label = Label(
            self.stopped_bar,
            text="Stopped early",
            bg="#2b1744",
            fg="#ff5c8a",
            font=self.get_font("Segoe UI", size_offset=-4, weight="bold"),  # Slightly smaller than base font
        )
        self.stopped_label.pack(padx=6, pady=4)

        self.terminal_scrollbar = ttk.Scrollbar(
            self.terminal_content, orient='vertical', style='Purple.Vertical.TScrollbar'
        )
        self.terminal_scrollbar.pack(side='right', fill='y')

        self.terminal = Text(
            self.terminal_content, height=15, width=60, wrap='word',
            yscrollcommand=self.terminal_scrollbar.set, state=DISABLED,
            bg=self.colors["terminal_bg"], fg=self.colors["terminal_fg"]
        )
        self.terminal.pack(side='left', fill='both', expand=True)
        self.terminal_scrollbar.config(command=self.terminal.yview)

        # Progress widget
        self.progress = StickFigureKeyLockProgress(self.right_frame, width=820, height=160, 
                                                font_size=self.font_size)
        self.progress.pack(fill='x', pady=12)

    # Note: banner is managed inside terminal_frame via _show_stopped_banner()

        # Action buttons row
        self.actions_frame = Frame(self.right_frame, bg=self.colors["panel"])
        self.actions_frame.pack(pady=10)
        self.verify_button = ttk.Button(self.actions_frame, text="Start", command=self.verify_hash, style='Purple.TButton')
        self.verify_button.grid(row=0, column=0, padx=(0, 8))
        self.stop_button = ttk.Button(self.actions_frame, text="Stop", command=self.stop_verification, style='Purple.TButton')
        self.stop_button.grid(row=0, column=1)
        self.stop_button.state(["disabled"])  # disabled initially
        self.actions_frame.columnconfigure(0, weight=0)
        self.actions_frame.columnconfigure(1, weight=0)

        # Progress update throttling state
        self._progress_last_ts = 0.0
        self._progress_last_frac = 0.0

    def on_drop_hash(self, event):
        try:
            file_path = event.data.strip("{}")  # handles spaces in file paths
            
            # Validate that the file exists
            if not os.path.exists(file_path):
                self.append_terminal(f"Error: File not found - {file_path}", color="#ff6b6b")
                return
            
            # Check if it's a file (not a directory)
            if not os.path.isfile(file_path):
                self.append_terminal(f"Error: Not a file - {file_path}", color="#ff6b6b")
                return
            
            # Update the entry field
            self.hash_entry.delete(0, END)
            self.hash_entry.insert(0, file_path)
            self.hash_entry.config(fg=self.colors["entry_fg"], justify='left')
            self.showing_placeholder = False
            
            # Show success feedback in terminal
            filename = os.path.basename(file_path)
            self.append_terminal(f"Hash file imported: {filename}", color="#90ee90")
            
        except Exception as e:
            # Show error feedback in terminal
            self.append_terminal(f"Error importing hash file: {str(e)}", color="#ff6b6b")

    def on_drop_wordlist(self, event):
        """Handle drag and drop for wordlist files"""
        try:
            file_path = event.data.strip("{}")  # handles spaces in file paths
            
            # Validate that the file exists
            if not os.path.exists(file_path):
                self.append_terminal(f"Error: Wordlist file not found - {file_path}", color="#ff6b6b")
                return
            
            # Check if it's a file (not a directory)
            if not os.path.isfile(file_path):
                self.append_terminal(f"Error: Not a file - {file_path}", color="#ff6b6b")
                return
            
            # Import the wordlist using the existing import functionality
            import shutil
            
            # Get the wordlists directory path
            wordlists_dir = os.path.join(os.path.dirname(__file__), "wordlists")
            
            # Ensure wordlists directory exists
            os.makedirs(wordlists_dir, exist_ok=True)
            
            # Get the filename from the path
            filename = os.path.basename(file_path)
            destination = os.path.join(wordlists_dir, filename)
            
            # Check if file already exists
            if os.path.exists(destination):
                # Add a timestamp to make it unique
                import time
                timestamp = int(time.time())
                name, ext = os.path.splitext(filename)
                filename = f"{name}_{timestamp}{ext}"
                destination = os.path.join(wordlists_dir, filename)
            
            # Copy the file
            shutil.copy2(file_path, destination)
            
            # Reload the wordlist display
            self.reload_wordlists()
            
            # Show success message in terminal
            self.append_terminal(f"Wordlist imported: {filename}", color="#90ee90")

        except Exception as e:
            # Show error feedback in terminal
            self.append_terminal(f"Error importing wordlist via drag & drop: {str(e)}", color="#ff6b6b")

    def _on_entry_focus_in(self, event):
        """Handle entry field focus in - clear placeholder text"""
        if self.showing_placeholder:
            self.hash_entry.delete(0, END)
            self.hash_entry.config(fg=self.colors["entry_fg"], justify='left')
            self.showing_placeholder = False

    def _on_entry_focus_out(self, event):
        """Handle entry field focus out - restore placeholder if empty"""
        if not self.hash_entry.get().strip():
            self.showing_placeholder = True
            # Trigger the placeholder update
            self.hash_entry.after_idle(lambda: (
                self.hash_entry.delete(0, END),
                self.hash_entry.insert(0, "Double-click to browse file"),
                self.hash_entry.config(fg=self.colors["muted"], justify='center')
            ))

    def browse_hash_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Hash File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            self.hash_entry.delete(0, END)
            self.hash_entry.insert(0, file_path)
            self.hash_entry.config(fg=self.colors["entry_fg"], justify='left')
            self.showing_placeholder = False

    def import_wordlist(self):
        """Import a user wordlist file to the wordlists directory"""
        file_path = filedialog.askopenfilename(
            title="Select Wordlist File to Import",
            filetypes=[
                ("Text Files", "*.txt"),
                ("Word Files", "*.lst"),
                ("Dictionary Files", "*.dict"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            try:
                import shutil
                # Get the wordlists directory path
                wordlists_dir = os.path.join(os.path.dirname(__file__), "wordlists")
                
                # Ensure wordlists directory exists
                os.makedirs(wordlists_dir, exist_ok=True)
                
                # Get the filename from the path
                filename = os.path.basename(file_path)
                destination = os.path.join(wordlists_dir, filename)
                
                # Check if file already exists
                if os.path.exists(destination):
                    # Add a timestamp to make it unique
                    import time
                    timestamp = int(time.time())
                    name, ext = os.path.splitext(filename)
                    filename = f"{name}_{timestamp}{ext}"
                    destination = os.path.join(wordlists_dir, filename)
                
                # Copy the file
                shutil.copy2(file_path, destination)
                
                # Reload the wordlist display
                self.reload_wordlists()
                
                # Show success message in terminal
                self.append_terminal(f"Successfully imported wordlist: {filename}", color="#90ee90")
                
            except Exception as e:
                # Show error message in terminal
                self.append_terminal(f"Error importing wordlist: {str(e)}", color="#ff6b6b")

    def reload_wordlists(self):
        """Reload the wordlist display"""
        # Clear current items
        self.wordlist_box.delete(0, END)
        
        # Reload wordlists
        self.load_wordlists()
        
        # Update tooltip visibility
        if hasattr(self, '_update_wordlist_tooltip'):
            self._update_wordlist_tooltip()

    def load_wordlists(self):
        """
        Load and display all available wordlists in the selection box.
        
        This method scans the wordlists directory and populates the
        wordlist selection box with all available .txt files. It also
        updates tooltip visibility for user guidance.
        
        Called during initialization and after importing new wordlists.
        """
        wordlists = get_available_wordlists()
        for wordlist in wordlists:
            self.wordlist_box.insert(END, wordlist)
        
        # Update tooltip visibility after loading
        if hasattr(self, '_update_wordlist_tooltip'):
            self._update_wordlist_tooltip()

    def append_terminal(self, text, replace_last=False, color="#e6d9ff", segments=None):
        """
        Optimized terminal append with tag caching and batched updates.
        """
        # Add to pending updates for batching
        self._pending_terminal_updates.append((text, replace_last, color, segments))
        
        # Schedule batch update if not already scheduled
        if not self._terminal_update_scheduled:
            self._terminal_update_scheduled = True
            self.master.after_idle(self._process_terminal_updates)

    def _process_terminal_updates(self):
        """
        Process all pending terminal updates in a single batch for better performance.
        """
        if not self._pending_terminal_updates:
            self._terminal_update_scheduled = False
            return
            
        self.terminal.config(state=NORMAL)
        
        # Process all pending updates
        for text, replace_last, color, segments in self._pending_terminal_updates:
            if replace_last:
                last_line_idx = self.terminal.index("end-2l")
                self.terminal.delete(last_line_idx, "end-1l")
                
            if segments:
                for seg_text, seg_color in segments:
                    tag_name = self._get_or_create_tag(seg_color)
                    self.terminal.insert(END, seg_text, tag_name)
                self.terminal.insert(END, "\n")
            else:
                tag_name = self._get_or_create_tag(color)
                self.terminal.insert(END, text + "\n", tag_name)
        
        # Clear pending updates
        self._pending_terminal_updates.clear()
        self._terminal_update_scheduled = False
        
        # Single scroll and state update for all messages
        self.terminal.see(END)
        self.terminal.config(state=DISABLED)

    def _get_or_create_tag(self, color):
        """
        Get cached color tag or create new one. Significant performance improvement
        over creating tags repeatedly for the same colors.
        """
        tag_name = f"color_{color.lstrip('#')}"
        
        # Check cache first (O(1) lookup)
        if tag_name not in self._terminal_tags_cache:
            # Create tag only if it doesn't exist
            if tag_name not in self.terminal.tag_names():
                self.terminal.tag_configure(tag_name, foreground=color)
            self._terminal_tags_cache[tag_name] = True
            
        return tag_name

    def clear_terminal(self):
        """
        Optimized terminal clear with cache reset.
        """
        # Clear any pending updates first
        self._pending_terminal_updates.clear()
        self._terminal_update_scheduled = False
        
        # Clear terminal content efficiently
        self.terminal.config(state=NORMAL)
        self.terminal.delete("1.0", END)
        self.terminal.see(END)
        self.terminal.config(state=DISABLED)
        
        # Reset tag cache for clean state
        self._terminal_tags_cache.clear()

    def update_progress(self, value, maximum):
        """
        Optimized progress update with better throttling and reduced UI calls.
        """
        try:
            maxv = float(maximum) if float(maximum) > 0 else 1.0
            frac = min(1.0, max(0.0, float(value) / maxv))
            now = time.monotonic()
            
            # Enhanced throttling: only update if significant change or enough time passed
            if frac < 1.0:
                time_diff = now - self._progress_last_ts
                frac_diff = frac - self._progress_last_frac
                
                # More aggressive throttling: require either significant time OR significant progress
                if time_diff < 0.1 and frac_diff < 0.02:
                    return
                    
            self._progress_last_ts = now
            self._progress_last_frac = frac
            
            # Single progress update
            self.progress.set(frac * 100.0)
            
            # Reduce update_idletasks calls - only when necessary
            if frac >= 1.0 or (now - getattr(self, '_last_ui_update', 0)) > 0.2:
                self.master.update_idletasks()
                self._last_ui_update = now
                
        except Exception:
            pass

    def verify_hash(self):
        """
        Start the hash verification process using selected wordlists.
        
        This is the main action method that:
        1. Validates user input (hash value and wordlist selection)
        2. Prepares the UI for verification (clears terminal, resets progress)
        3. Creates a background worker thread to perform the verification
        4. Updates button states to reflect the running process
        
        The actual verification work is done in a separate thread to keep
        the GUI responsive while processing potentially large wordlists.
        """
        hash_value = self.hash_entry.get()
        selected_indices = self.wordlist_box.curselection()
        selected_wordlists = [self.wordlist_box.get(i) for i in selected_indices]

        if not hash_value:
            self.append_terminal("Input Error: Please enter a hash value or path to a hash file.")
            return

        if not selected_wordlists:
            self.append_terminal("Input Error: Please select at least one wordlist.")
            return

        # Refresh the terminal on each start
        self.clear_terminal()

        self.append_terminal("Starting hash verification...")
        # Ensure any previous 'stopped' banner is hidden at start
        self._show_stopped_banner(False)
        self._progress_last_ts = 0.0
        self._progress_last_frac = 0.0
        self.progress.reset()
        self.progress.start()
        self._stop_event = threading.Event()
        
        # Optimized: batch button state changes
        self._update_button_states(verify_enabled=False, stop_enabled=True)

        self._worker_thread = threading.Thread(
            target=self._run_verify_hash,
            args=(hash_value, selected_wordlists),
            daemon=True
        )
        self._worker_thread.start()

    def _update_button_states(self, verify_enabled=True, stop_enabled=False):
        """
        Optimized method to update button states in a single batch operation.
        Reduces multiple widget state changes to a single call.
        """
        try:
            if verify_enabled:
                self.verify_button.state(["!disabled"])
            else:
                self.verify_button.state(["disabled"])
                
            if stop_enabled:
                self.stop_button.state(["!disabled"])
            else:
                self.stop_button.state(["disabled"])
        except Exception:
            pass

    def _show_stopped_banner(self, show=True):
        if show:
            # Pack at the bottom of the terminal area
            self.stopped_bar.pack(side='bottom', fill='x')
        else:
            self.stopped_bar.pack_forget()

    def _run_verify_hash(self, hash_value, selected_wordlists):
        result = verify_hash(
            hash_value,
            selected_wordlists,
            gui_callback=self._threadsafe_append_terminal,
            progress_callback=self._threadsafe_update_progress,
            stop_event=self._stop_event
        )
        def finish():
            if self._stop_event and self._stop_event.is_set():
                self.progress.stop()
                self._show_stopped_banner(True)
            else:
                self.progress.set(100.0)
                self.progress.celebrate(1200)
                self.master.after(1400, self.progress.stop)
                self._show_stopped_banner(False)
            
            # Optimized: batch button state changes
            self._update_button_states(verify_enabled=True, stop_enabled=False)
            self._worker_thread = None
        self.master.after(0, finish)

    def stop_verification(self):
        """
        Request to stop the current hash verification process.
        
        This method signals the worker thread to stop gracefully by setting
        a stop event. The thread will finish its current iteration and then
        exit cleanly. This prevents data corruption and ensures proper cleanup.
        
        Note: The stop is not immediate - it waits for the current password
        attempt to complete before stopping.
        """
        if self._stop_event and not self._stop_event.is_set():
            self._stop_event.set()
            self.append_terminal("Stopping… letting current iteration finish.")
            self._show_stopped_banner(False)

    def _threadsafe_append_terminal(self, text, replace_last=False, color="#e6d9ff", segments=None):
        # Marshal text updates safely to the Tk main loop
        self.master.after(0, self.append_terminal, text, replace_last, color, segments)

    def _threadsafe_update_progress(self, value, maximum):
        # Marshal progress updates safely to the Tk main loop
        self.master.after(0, self.update_progress, value, maximum)