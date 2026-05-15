<script lang="ts">
	const { title, showBack = false }: { title: string; showBack?: boolean } = $props();
</script>

<div class="mb-8 flex items-center justify-between">
	<h1 class="text-3xl font-bold text-gray-900">{title}</h1>
	<div>
		{#if showBack}
			<a
				href="/dashboard"
				class="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:outline-none"
			>
				Back to Dashboard
			</a>
		{/if}

		<a
			href="/dashboard/signout"
			class="rounded-md bg-gray-600 px-4 py-2 text-white hover:bg-gray-700 focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 focus:outline-none"
		>
			Sign Out
		</a>
	</div>
</div>
