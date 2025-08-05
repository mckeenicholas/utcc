<script lang="ts">
	const { message }: { message: string } = $props();
</script>

<div class="flex min-h-screen items-center justify-center">
	<div class="w-full max-w-md space-y-4 rounded-lg bg-gray-100 p-6 text-center shadow-md">
		<p class="text-lg font-medium">{message}</p>
		<div class="flex justify-center">
			<div
				class="h-6 w-6 animate-spin rounded-full border-2 border-gray-300 border-t-gray-600"
			></div>
		</div>
	</div>
</div>
