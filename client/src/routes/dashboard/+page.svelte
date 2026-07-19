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
	<LoadingScreen message="Loading Dashboard" />
{:else}
	<div class="min-h-screen bg-gray-50 py-8">
		<div class="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
			<!-- Header -->
			<DashboardHeader title="Dashboard" />

			<!-- Management Cards -->
			<div class="grid gap-6 md:grid-cols-2">
				<!-- Competition Management Card -->
				<a
					href="/dashboard/competitions"
					class="group block rounded-xl border border-gray-200 bg-white p-6 shadow-sm transition-all duration-200 hover:bg-gray-50/50 hover:shadow-md"
				>
					<div class="flex items-center space-x-3">
						<div>
							<h2 class="text-xl font-bold text-gray-900 transition-colors group-hover:text-blue-600">
								Competition Management
							</h2>
							<p class="mt-2 text-sm font-medium text-gray-500">Create, manage, and view competition results</p>
						</div>
					</div>
					<div class="mt-4 flex items-center text-blue-600 transition-colors group-hover:text-blue-700">
						<span class="text-sm font-semibold">Manage Competitions</span>
						<svg
							class="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
						>
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" />
						</svg>
					</div>
				</a>

				<!-- User Management Card -->
				<a
					href="/dashboard/users"
					class="group block rounded-xl border border-gray-200 bg-white p-6 shadow-sm transition-all duration-200 hover:bg-gray-50/50 hover:shadow-md"
				>
					<div class="flex items-center space-x-3">
						<div>
							<h2 class="text-xl font-bold text-gray-900 transition-colors group-hover:text-emerald-600">
								User Management
							</h2>
							<p class="mt-2 text-sm font-medium text-gray-500">Add, edit, and manage user accounts</p>
						</div>
					</div>
					<div class="mt-4 flex items-center text-emerald-600 transition-colors group-hover:text-emerald-700">
						<span class="text-sm font-semibold">Manage Users</span>
						<svg
							class="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
						>
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" />
						</svg>
					</div>
				</a>

				<!-- Session Management Card -->
				<a
					href="/dashboard/sessions"
					class="group block rounded-xl border border-gray-200 bg-white p-6 shadow-sm transition-all duration-200 hover:bg-gray-50/50 hover:shadow-md"
				>
					<div class="flex items-center space-x-3">
						<div>
							<h2 class="text-xl font-bold text-gray-900 transition-colors group-hover:text-orange-500">
								Session Management
							</h2>
							<p class="mt-2 text-sm font-medium text-gray-500">Add, edit, and manage academic sessions</p>
						</div>
					</div>
					<div class="mt-4 flex items-center text-orange-500 transition-colors group-hover:text-orange-600">
						<span class="text-sm font-semibold">Manage Sessions</span>
						<svg
							class="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
						>
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" />
						</svg>
					</div>
				</a>
			</div>
		</div>
	</div>
{/if}
