---
name: Manim Presentation Layout Guidelines
description: Best practices for avoiding layout anti-patterns in Manim animations, ensuring readability and preventing overlaps.
---

# Manim Presentation Layout Guidelines

This skill defines the rules to follow when creating Manim animations for presentations or explainer videos, specifically to avoid common pitfalls like overlapping elements and poor visibility.

## 🚨 Anti-Patterns (What to Avoid)

### 1. Overlapping with Structural Elements (Header/Footer)
**Problem**: Placing main content too high (`UP * 2.0` or more) or too low (`DOWN * 2.0` or more).
- **Result**: Objects clash with section titles (top) or subtitles (bottom).
- **Fix**: Keep main content within the "Safe Area" (approximately `UP * 1.5` to `DOWN * 1.5`).

### 2. Low Contrast Text on Shapes
**Problem**: Using white text (`color=WHITE`) on shapes with light fill colors (e.g., opacity 0.5 blue/red).
- **Result**: Text becomes unreadable.
- **Fix**: Use dark text colors (`TEXT_MAIN` or `#1a1a2e`) when placing text on light or transparent backgrounds. Increase shape opacity if necessary.

### 3. Ghost Objects via Transform
**Problem**: Using `Transform(m1, m2)` when `m1` and `m2` are conceptually different or temporary objects (like a label on a graph that disappears).
- **Result**: The original object might linger or transition weirdly, leaving artifacts in subsequent animations.
- **Fix**: Use `FadeOut(m1)` and `FadeIn(m2)` separately for cleaner state management.

### 4. Inconsistent Spacing (Manual Coordinates)
**Problem**: Manually setting positions like `obj1.move_to(UP*1.5)`, `obj2.move_to(UP*0.5)`.
- **Result**: Visual balance is often off, and grouping animations becomes harder.
- **Fix**: Group related objects into a `VGroup`, use `.arrange()`, and then move the entire group.

## ✅ Best Practices Code Examples

### Layout Safety
```python
# GOOD: Defining a safe area center
content_group = VGroup(chart, label)
content_group.arrange(DOWN, buff=0.5)
# Center the group slightly above ORIGIN to avoid subtitles, but below title
content_group.move_to(UP * 0.5) 
```

### High Visibility Text
```python
# GOOD: High contrast text on light background
bg_rect = Rectangle(color=BLUE, fill_opacity=0.3)
label = Text("Strong Contrast", color=TEXT_MAIN) # Dark color
label.move_to(bg_rect)
```

### Clean Transitions
```python
# GOOD: Explicit entry/exit
self.play(FadeOut(old_graph), run_time=0.5)
self.play(FadeIn(new_graph), run_time=0.5)
```

## Checklist Before Rendering
1.  [ ] Is the top 15% of the screen clear for titles?
2.  [ ] Is the bottom 20% of the screen clear for subtitles?
3.  [ ] Is text readable against its specific background?
4.  [ ] Are all objects grouped logically?
