import { writable } from "svelte/store";
import { browser } from "$app/environment";

export type Theme = "light" | "dark" | "system";

const STORAGE_KEY = "utcc-theme";

const getInitialTheme = (): Theme => {
	if (!browser) {
		return "system";
	}
	const stored = globalThis.localStorage.getItem(STORAGE_KEY);
	if (stored === "light" || stored === "dark" || stored === "system") {
		return stored;
	}
	return "system";
};

export const theme = writable<Theme>(getInitialTheme());

const applyTheme = (currentTheme: Theme) => {
	if (!browser) {
		return;
	}

	const isDark =
		currentTheme === "dark" ||
		(currentTheme === "system" && globalThis.matchMedia("(prefers-color-scheme: dark)").matches);

	document.documentElement.classList.toggle("dark", isDark);
};

if (browser) {
	theme.subscribe((value) => {
		globalThis.localStorage.setItem(STORAGE_KEY, value);
		applyTheme(value);
	});

	// Listen for system theme changes when in 'system' mode
	globalThis.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
		const stored = globalThis.localStorage.getItem(STORAGE_KEY) as Theme | null;
		if (!stored || stored === "system") {
			applyTheme("system");
		}
	});
}

export const setTheme = (newTheme: Theme) => {
	theme.set(newTheme);
};

export const toggleTheme = () => {
	theme.update((current) => {
		if (current === "light") {
			return "dark";
		}
		if (current === "dark") {
			return "system";
		}
		return "light";
	});
};
