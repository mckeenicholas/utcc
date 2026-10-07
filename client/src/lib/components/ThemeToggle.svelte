<script lang="ts">
import { setTheme, theme, type Theme } from "#lib/stores/theme.js";

interface Props {
	class?: string;
}

const { class: className = "" }: Props = $props();

const nextThemeMap: Record<Theme, Theme> = {
	dark: "system",
	light: "dark",
	system: "light",
};

const handleToggle = () => {
	setTheme(nextThemeMap[$theme]);
};
</script>

<button
	type="button"
	onclick={handleToggle}
	class="inline-flex h-8 items-center gap-1.5 rounded-sm border border-border bg-surface px-2.5 py-1 text-xs font-medium text-secondary transition-colors hover:border-border-strong hover:bg-surface-muted focus:outline-none focus-visible:ring-1 focus-visible:ring-brand {className}"
	title="Theme: {$theme} (click to switch to {nextThemeMap[$theme]})"
	aria-label="Theme: {$theme} (click to switch to {nextThemeMap[$theme]})"
>
	{#if $theme === "light"}
		<!-- Sun icon for light mode -->
		<svg class="h-3.5 w-3.5 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="2"
				d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
			/>
		</svg>
		<span class="text-[11px] font-semibold">Light</span>
	{:else if $theme === "dark"}
		<!-- Moon icon for dark mode -->
		<svg class="h-3.5 w-3.5 text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="2"
				d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
			/>
		</svg>
		<span class="text-[11px] font-semibold">Dark</span>
	{:else}
		<!-- Monitor / System icon -->
		<svg class="h-3.5 w-3.5 text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="2"
				d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
			/>
		</svg>
		<span class="text-[11px] font-semibold">System</span>
	{/if}
</button>
