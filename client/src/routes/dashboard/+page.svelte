<script lang="ts">
import { goto } from '$app/navigation';
import { onMount } from 'svelte';
import { checkLoginStatus } from '$lib/utils';
import DashboardHeader from '$lib/components/DashboardHeader.svelte';
import LoadingScreen from '$lib/components/LoadingScreen.svelte';

let loading = $state(true);

onMount(async () => {
	const loggedIn = await checkLoginStatus();

	if (!loggedIn) {
		goto('/dashboard/signin');
		return;
	}

	loading = false;
});
</script>

{#if loading}
	<LoadingScreen message="Loading Dashboard" />
{:else}
	<div class="min-h-screen py-8">
		<div class="mx-auto max-w-4xl px-4">
			<!-- Header -->
			<DashboardHeader title="Dashboard" />

			<!-- Management Cards -->
			<div class="grid gap-6 md:grid-cols-2">
				<!-- Competition Management Card -->
				<a
					href="/dashboard/competitions"
					class="group mb-4 block rounded-lg bg-white p-6 shadow-sm transition-all hover:bg-gray-50 hover:shadow-md"
				>
					<div class="flex items-center space-x-3">
						<div>
							<h2
								class="text-xl font-semibold text-gray-900 transition-colors group-hover:text-blue-600"
							>
								Competition Management
							</h2>
							<p class="mt-1 text-sm text-gray-600">Create, manage, and view competition results</p>
						</div>
					</div>
					<div
						class="mt-4 flex items-center text-blue-600 transition-colors group-hover:text-blue-700"
					>
						<span class="text-sm font-medium">Manage Competitions</span>
						<svg class="ml-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M9 5l7 7-7 7"
							/>
						</svg>
					</div>
				</a>

				<!-- User Management Card -->
				<a
					href="/dashboard/users"
					class="group block rounded-lg bg-white p-6 shadow-sm transition-all hover:bg-gray-50 hover:shadow-md"
				>
					<div class="flex items-center space-x-3">
						<div>
							<h2
								class="text-xl font-semibold text-gray-900 transition-colors group-hover:text-green-600"
							>
								User Management
							</h2>
							<p class="mt-1 text-sm text-gray-600">Add, edit, and manage user accounts</p>
						</div>
					</div>
					<div
						class="mt-4 flex items-center text-green-600 transition-colors group-hover:text-green-700"
					>
						<span class="text-sm font-medium">Manage Users</span>
						<svg class="ml-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M9 5l7 7-7 7"
							/>
						</svg>
					</div>
				</a>
			</div>
		</div>
	</div>
{/if}
