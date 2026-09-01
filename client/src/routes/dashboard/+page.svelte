<script lang="ts">
import { onMount } from "svelte";
import { goto } from "$app/navigation";
import DashboardHeader from "$lib/components/DashboardHeader.svelte";
import LoadingScreen from "$lib/components/LoadingScreen.svelte";
import { checkLoginStatus } from "$lib/utils";

let loading = $state(true);

onMount(async () => {
	const loggedIn = await checkLoginStatus();

	if (!loggedIn) {
		goto("/dashboard/signin");
		return;
	}

	loading = false;
});
</script>

{#if loading}
	<div class="py-16 text-center">
		<LoadingScreen message="Loading Dashboard..." inline />
	</div>
{:else}
	<div class="py-8 pb-16">
		<div class="mx-auto max-w-5xl px-4 sm:px-6">
			<!-- Header -->
			<DashboardHeader title="Club Administration" />

			<!-- Management Cards -->
			<div class="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
				<!-- Competition Management Card -->
				<a
					href="/dashboard/competitions"
					class="group flex flex-col justify-between border border-gray-200 bg-white p-5 transition-colors hover:border-uoft-blue"
				>
					<div>
						<div
							class="flex h-8 w-8 items-center justify-center rounded-sm bg-gray-100 text-uoft-blue transition-colors group-hover:bg-uoft-blue group-hover:text-white"
						>
							<span class="cubing-icon event-333 text-base"></span>
						</div>
						<h2 class="mt-3 text-base font-bold text-gray-900 transition-colors group-hover:text-uoft-blue">
							Competitions
						</h2>
						<p class="mt-1 text-xs text-gray-700">Create, manage, and enter competition solve results.</p>
					</div>
					<div
						class="mt-4 flex items-center text-xs font-semibold text-uoft-blue transition-colors group-hover:text-secondary-cyan"
					>
						Manage Competitions &rarr;
					</div>
				</a>

				<!-- User Management Card -->
				<a
					href="/dashboard/users"
					class="group flex flex-col justify-between border border-gray-200 bg-white p-5 transition-colors hover:border-uoft-blue"
				>
					<div>
						<div
							class="flex h-8 w-8 items-center justify-center rounded-sm bg-gray-100 text-uoft-blue transition-colors group-hover:bg-uoft-blue group-hover:text-white"
						>
							<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
								/>
							</svg>
						</div>
						<h2 class="mt-3 text-base font-bold text-gray-900 transition-colors group-hover:text-uoft-blue">
							Members & Users
						</h2>
						<p class="mt-1 text-xs text-gray-700">Register new competitors and edit student status.</p>
					</div>
					<div
						class="mt-4 flex items-center text-xs font-semibold text-uoft-blue transition-colors group-hover:text-secondary-cyan"
					>
						Manage Users &rarr;
					</div>
				</a>

				<!-- Session Management Card -->
				<a
					href="/dashboard/sessions"
					class="group flex flex-col justify-between border border-gray-200 bg-white p-5 transition-colors hover:border-uoft-blue"
				>
					<div>
						<div
							class="flex h-8 w-8 items-center justify-center rounded-sm bg-gray-100 text-uoft-blue transition-colors group-hover:bg-uoft-blue group-hover:text-white"
						>
							<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
								/>
							</svg>
						</div>
						<h2 class="mt-3 text-base font-bold text-gray-900 transition-colors group-hover:text-uoft-blue">
							Academic Sessions
						</h2>
						<p class="mt-1 text-xs text-gray-700">Configure Fall, Winter, and Summer term periods.</p>
					</div>
					<div
						class="mt-4 flex items-center text-xs font-semibold text-uoft-blue transition-colors group-hover:text-secondary-cyan"
					>
						Manage Sessions &rarr;
					</div>
				</a>
			</div>
		</div>
	</div>
{/if}
