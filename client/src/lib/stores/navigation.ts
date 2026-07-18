import { writable } from "svelte/store";

// This is used as a hacky way to "see" if the users last
// Page was on this site, by keeping track of their "page depth"
export const navigationCount = writable<number>(0);

export const incrementNavigationCount = () => {
	navigationCount.update((count) => count + 1);
};

export const decrementNavigationCount = (amount = 1) => {
	navigationCount.update((count) => Math.max(0, count - amount));
};
