<script lang="ts">
import { page } from "$app/state";

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

<header class="border-b border-gray-200 bg-white">
	<div class="mx-auto max-w-6xl px-4 sm:px-6">
		<div class="flex h-16 items-center justify-between">
			<!-- Brand Logo & Title -->
			<div class="flex items-center gap-6">
				<a href="/" class="flex items-center gap-2.5 transition-opacity hover:opacity-90">
					<img src="/client-static/logo.png" alt="U of T Cube Club Logo" class="h-8 w-8 rounded-full object-contain" />
					<div>
						<span class="block text-base font-bold tracking-tight text-uoft-blue sm:text-lg"> U of T Cube Club </span>
					</div>
				</a>

				<!-- Desktop Nav Links -->
				<nav class="hidden md:flex md:items-center md:gap-1">
					{#each navItems as item (item.href)}
						{@const active = isActive(item.href)}
						<a
							href={item.href}
							class="px-3 py-5 text-sm font-medium transition-colors {active
								? 'border-b-2 border-uoft-blue font-semibold text-uoft-blue'
								: 'border-b-2 border-transparent text-gray-600 hover:border-gray-300 hover:text-gray-900'}"
						>
							{item.label}
						</a>
					{/each}
				</nav>
			</div>

			<!-- Mobile Menu Button -->
			<div class="flex items-center sm:hidden">
				<button
					type="button"
					onclick={() => (mobileMenuOpen = !mobileMenuOpen)}
					class="rounded-sm p-2 text-gray-600 hover:bg-gray-100 hover:text-gray-900 focus:outline-none"
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
			</div>
		</div>
	</div>

	<!-- Mobile Nav Drawer -->
	{#if mobileMenuOpen}
		<div class="border-t border-gray-200 bg-white px-4 py-3 sm:hidden">
			<nav class="flex flex-col gap-1">
				{#each navItems as item (item.href)}
					{@const active = isActive(item.href)}
					<a
						href={item.href}
						onclick={() => (mobileMenuOpen = false)}
						class="rounded-sm px-3 py-2 text-sm font-medium transition-colors {active
							? 'bg-gray-100 font-semibold text-uoft-blue'
							: 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'}"
					>
						{item.label}
					</a>
				{/each}
			</nav>
		</div>
	{/if}
</header>
