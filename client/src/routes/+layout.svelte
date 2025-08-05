<script lang="ts">
	import '../app.css';
	let { children } = $props();
</script>

{@render children()}

<style>
	:global(html) {
		background-color: rgb(249 250 251);
	}
</style>
