<template>
	<apexchart
		type="area"
		height="350"
		:series="series"
		:options="options"
	></apexchart>

	{{ options }}-{{ series }}
</template>

<script>
export default {
	props: {
		series: { type: Array },
		options: { type: Object },
	},
	name: "myChart",
	data() {
		return {};
	},
};
</script>
