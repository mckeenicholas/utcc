<script lang="ts">
import { page } from "$app/state";
import ThemeToggle from "./ThemeToggle.svelte";

let mobileMenuOpen = $state(false);

const navItems = [
	{ href: "/results", label: "Results" },
	{ href: "/records", label: "Records" },
	{ href: "/rankings", label: "Rankings" },
	{ href: "/competitions", label: "Competitions" },
	{ href: "/persons", label: "Competitors" },
];

const isActive = (href: string) => {
	const { pathname } = page.url;
	if (href === "/results") {
		return pathname === "/results" || (pathname.startsWith("/competitions/") && pathname.endsWith("/results"));
	}
	return pathname === href || pathname.startsWith(`${href}/`);
};
</script>

<header class="border-b border-border bg-surface transition-colors">
	<div class="flex h-16 w-full items-center justify-between px-4 sm:px-6">
		<!-- Brand Logo & Title -->
		<div class="flex items-center gap-6">
			<a href="/" class="flex items-center gap-2.5 transition-opacity hover:opacity-90">
				<img src="/client-static/logo.png" alt="U of T Cube Club Logo" class="h-8 w-8 rounded-full object-contain" />
				<div>
					<span class="block text-base font-bold tracking-tight text-brand transition-colors sm:text-lg">
						U of T Cube Club
					</span>
				</div>
			</a>

			<!-- Desktop Nav Links -->
			<nav class="hidden md:flex md:items-center md:gap-1">
				{#each navItems as item (item.href)}
					{@const active = isActive(item.href)}
					<a
						href={item.href}
						class="px-3 py-5 text-sm font-medium transition-colors {active
							? 'border-b-2 border-brand font-semibold text-brand'
							: 'border-b-2 border-transparent text-secondary hover:border-border-strong hover:text-main'}"
					>
						{item.label}
					</a>
				{/each}
			</nav>
		</div>

		<!-- Right side: Mobile Menu Button & Theme Toggle (all the way in the corner) -->
		<div class="flex items-center gap-2">
			<!-- Mobile Menu Button -->
			<button
				type="button"
				onclick={() => (mobileMenuOpen = !mobileMenuOpen)}
				class="rounded-sm p-2 text-secondary hover:bg-surface-muted hover:text-main focus:outline-none sm:hidden"
				aria-label="Toggle Navigation Menu"
			>
				<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					{#if mobileMenuOpen}
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
					{:else}
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
					{/if}
				</svg>
			</button>

			<ThemeToggle />
		</div>
	</div>

	<!-- Mobile Nav Drawer -->
	{#if mobileMenuOpen}
		<div class="border-t border-border bg-surface px-4 py-3 sm:hidden">
			<nav class="flex flex-col gap-1">
				{#each navItems as item (item.href)}
					{@const active = isActive(item.href)}
					<a
						href={item.href}
						onclick={() => (mobileMenuOpen = false)}
						class="rounded-sm px-3 py-2 text-sm font-medium transition-colors {active
							? 'bg-surface-muted font-semibold text-brand'
							: 'text-secondary hover:bg-surface-muted hover:text-main'}"
					>
						{item.label}
					</a>
				{/each}
			</nav>
		</div>
	{/if}
</header>
