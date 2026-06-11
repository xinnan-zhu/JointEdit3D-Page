const COMPARE_CASES = [
  {
    id: "360usid_10000_40step_gen_0004_original_f000",
    label: "360-USID",
    title: "360-USID Example 01",
    prompt: "Remove the bear from the scene.",
    beforeLabel: "Source",
    afterLabel: "JointEdit3D",
    before: "assets/media/inference/360usid_10000_40step_gen_0004_original_f000_source.mp4",
    after: "assets/media/inference/360usid_10000_40step_gen_0004_original_f000_edited.mp4",
    model: "assets/models/inference/assert_001.glb",
    modelLabel: "3D",
    cameraOrbit: "154.7deg 82.9deg auto",
    modelOrientation: "180deg 0deg 0deg"
  },
  {
    id: "demo_hint_vis_sample002_0001_original_f024",
    label: "ScanNetPP-case",
    title: "ScanNetPP-case Example 02",
    prompt: "Remove only the right wall painting, the square dark artwork with the bright orange/yellow circle on the beige wall.",
    beforeLabel: "Source",
    afterLabel: "JointEdit3D",
    before: "assets/media/inference/demo_hint_vis_sample002_0001_original_f024_source.mp4",
    after: "assets/media/inference/demo_hint_vis_sample002_0001_original_f024_edited.mp4",
    model: "assets/models/inference/assert_002.glb",
    modelLabel: "3D",
    cameraOrbit: "168.2deg 88.0deg auto",
    modelOrientation: "180deg 0deg 0deg"
  },
  {
    id: "edit_bench_10000_40step_0013_original_f045",
    label: "SceneEdit3D",
    title: "SceneEdit3D Example 04",
    prompt: "Add a cluster of grey computer equipment, including a monitor, speakers, and tangled cables, to the floor in the corner next to the blue barrel.",
    beforeLabel: "Source",
    afterLabel: "JointEdit3D",
    before: "assets/media/inference/edit_bench_10000_40step_0013_original_f045_source.mp4",
    after: "assets/media/inference/edit_bench_10000_40step_0013_original_f045_edited.mp4",
    model: "assets/models/inference/assert_003.glb",
    modelLabel: "3D",
    cameraOrbit: "162.6deg 88.0deg auto",
    modelOrientation: "180deg 0deg 0deg"
  },
  {
    id: "edit_bench_10000_40step_0063_original_f038",
    label: "SceneEdit3D",
    title: "SceneEdit3D Example 05",
    prompt: "Move the beige textured bean bag chair slightly to the right and further back into the corner of the room, creating more open floor space near the easel.",
    beforeLabel: "Source",
    afterLabel: "JointEdit3D",
    before: "assets/media/inference/edit_bench_10000_40step_0063_original_f038_source.mp4",
    after: "assets/media/inference/edit_bench_10000_40step_0063_original_f038_edited.mp4",
    model: "assets/models/inference/assert_004.glb",
    modelLabel: "3D",
    cameraOrbit: "-164.7deg 87.1deg auto",
    modelOrientation: "180deg 0deg 0deg"
  },
  {
    id: "my_tests_10000_10step_0000_original_f024",
    label: "Custom",
    title: "Custom Example 07",
    prompt: "Remove the leftmost flower pot",
    beforeLabel: "Source",
    afterLabel: "JointEdit3D",
    before: "assets/media/inference/my_tests_10000_10step_0000_original_f024_source.mp4",
    after: "assets/media/inference/my_tests_10000_10step_0000_original_f024_edited.mp4",
    model: "assets/models/inference/assert_005.glb",
    modelLabel: "3D",
    cameraOrbit: "-178.5deg 88.0deg auto",
    modelOrientation: "180deg 0deg 0deg"
  },
  {
    id: "my_tests_10000_10step_0006_original_f024",
    label: "Custom",
    title: "Custom Example 09",
    prompt: "Add a metal spatula with a wooden handle on the round table beside the tea tray.",
    beforeLabel: "Source",
    afterLabel: "JointEdit3D",
    before: "assets/media/inference/my_tests_10000_10step_0006_original_f024_source.mp4",
    after: "assets/media/inference/my_tests_10000_10step_0006_original_f024_edited.mp4",
    model: "assets/models/inference/assert_006.glb",
    modelLabel: "3D",
    cameraOrbit: "-166.0deg 88.0deg auto",
    modelOrientation: "180deg 0deg 0deg"
  },
  {
    id: "scannetpp_case_10000_40step_0002_original_f024",
    label: "ScanNetPP-case",
    title: "ScanNetPP-case Example 10",
    prompt: "Remove all computer monitors, computer stands, keyboards, and visible computer cables from the white cabinet/table, while keeping the small bottle on the right side.",
    beforeLabel: "Source",
    afterLabel: "JointEdit3D",
    before: "assets/media/inference/scannetpp_case_10000_40step_0002_original_f024_source.mp4",
    after: "assets/media/inference/scannetpp_case_10000_40step_0002_original_f024_edited.mp4",
    model: "assets/models/inference/assert_007.glb",
    modelLabel: "3D",
    cameraOrbit: "170.6deg 87.0deg auto",
    modelOrientation: "180deg 0deg 0deg"
  },
  {
    id: "scannetpp_case_10000_40step_0004_original_f036",
    label: "ScanNetPP-case",
    title: "ScanNetPP-case Example 11",
    prompt: "Add one white front-loading washing machine on the tiled floor against the wall, immediately to the left of the potted plant.",
    beforeLabel: "Source",
    afterLabel: "JointEdit3D",
    before: "assets/media/inference/scannetpp_case_10000_40step_0004_original_f036_source.mp4",
    after: "assets/media/inference/scannetpp_case_10000_40step_0004_original_f036_edited.mp4",
    model: "assets/models/inference/assert_008.glb",
    modelLabel: "3D",
    cameraOrbit: "166.3deg 81.0deg auto",
    modelOrientation: "180deg 0deg 0deg"
  },
  {
    id: "scannetpp_case_10000_40step_0005_original_f024",
    label: "ScanNetPP-case",
    title: "ScanNetPP-case Example 12",
    prompt: "Add one medium-sized plush teddy bear toy sitting on the center cushion of the brown sofa.",
    beforeLabel: "Source",
    afterLabel: "JointEdit3D",
    before: "assets/media/inference/scannetpp_case_10000_40step_0005_original_f024_source.mp4",
    after: "assets/media/inference/scannetpp_case_10000_40step_0005_original_f024_edited.mp4",
    model: "assets/models/inference/assert_009.glb",
    modelLabel: "3D",
    cameraOrbit: "168.4deg 87.3deg auto",
    modelOrientation: "180deg 0deg 0deg"
  },
  {
    id: "scannetpp_case_10000_40step_0006_original_f024",
    label: "ScanNetPP-case",
    title: "ScanNetPP-case Example 13",
    prompt: "Remove the front-facing galaxy poster on the left wall above the bed, and add one light-colored pillow on top of the black bed near the wooden headboard.",
    beforeLabel: "Source",
    afterLabel: "JointEdit3D",
    before: "assets/media/inference/scannetpp_case_10000_40step_0006_original_f024_source.mp4",
    after: "assets/media/inference/scannetpp_case_10000_40step_0006_original_f024_edited.mp4",
    model: "assets/models/inference/assert_010.glb",
    modelLabel: "3D",
    cameraOrbit: "178.8deg 81.5deg auto",
    modelOrientation: "180deg 0deg 0deg"
  },
  {
    id: "scannetpp_case_10000_40step_0007_original_f024",
    label: "ScanNetPP-case",
    title: "ScanNetPP-case Example 14",
    prompt: "Move the red office chair from under the desk on the left side to the area beside the white closet door near the center-right wall.",
    beforeLabel: "Source",
    afterLabel: "JointEdit3D",
    before: "assets/media/inference/scannetpp_case_10000_40step_0007_original_f024_source.mp4",
    after: "assets/media/inference/scannetpp_case_10000_40step_0007_original_f024_edited.mp4",
    model: "assets/models/inference/assert_011.glb",
    modelLabel: "3D",
    cameraOrbit: "179.2deg 88.0deg auto",
    modelOrientation: "180deg 0deg 0deg"
  },
  {
    id: "dggt_infer_ready_10000_10step_0001_original_f020",
    label: "DGGT Video",
    title: "DGGT Video Example 15",
    prompt: "Remove the camel from the zoo enclosure.",
    beforeLabel: "Source",
    afterLabel: "JointEdit3D",
    before: "assets/media/inference/dggt_infer_ready_10000_10step_0001_original_f020_source.mp4",
    after: "assets/media/inference/dggt_infer_ready_10000_10step_0001_original_f020_edited.mp4",
    model: "assets/models/inference/assert_012.glb",
    modelLabel: "3D",
    cameraOrbit: "172.6deg 88.0deg auto",
    modelOrientation: "180deg 0deg 0deg"
  },
  {
    id: "dggt_infer_ready_10000_10step_0003_original_f024",
    label: "DGGT Video",
    title: "DGGT Video Example 16",
    prompt: "Change the walking person's backpack to red.",
    beforeLabel: "Source",
    afterLabel: "JointEdit3D",
    before: "assets/media/inference/dggt_infer_ready_10000_10step_0003_original_f024_source.mp4",
    after: "assets/media/inference/dggt_infer_ready_10000_10step_0003_original_f024_edited.mp4",
    model: "assets/models/inference/assert_013.glb",
    modelLabel: "3D",
    cameraOrbit: "171.2deg 88.0deg auto",
    modelOrientation: "180deg 0deg 0deg"
  }
]

const DATASET_SAMPLES = [
  {
    id: "add_bathroom_01_task_0004_add_17_SM_Sink_Bathroom_view_0",
    label: "Add",
    title: "Add in Bathroom 01",
    prompt: "Add a wooden vanity with two dark grey stone vessel sinks and black faucets against the white marble wall, positioned between the stool and the bathtub.",
    before: "assets/media/dataset/add_bathroom_01_task_0004_add_17_SM_Sink_Bathroom_view_0_before.mp4",
    after: "assets/media/dataset/add_bathroom_01_task_0004_add_17_SM_Sink_Bathroom_view_0_after.mp4",
    sourceModel: "assets/models/dataset/add_bathroom_01_task_0004_add_17_SM_Sink_Bathroom_view_0_before.glb",
    editedModel: "assets/models/dataset/add_bathroom_01_task_0004_add_17_SM_Sink_Bathroom_view_0_after.glb",
    thumb: "assets/thumbs/dataset/add_bathroom_01_task_0004_add_17_SM_Sink_Bathroom_view_0_thumb.jpg",
    promptFrame: "assets/thumbs/dataset/add_bathroom_01_task_0004_add_17_SM_Sink_Bathroom_view_0_prompt_frame.jpg",
    usedFixMask: false,
    cameraOrbit: "15.0deg 88.0deg auto"
  },
  {
    id: "add_bedroom_21_task_0010_add_12_SM_Radio_view_0",
    label: "Add",
    title: "Add in Bedroom 21",
    prompt: "Add a vintage-style brown radio to the top shelf of the wooden bookcase.",
    before: "assets/media/dataset/add_bedroom_21_task_0010_add_12_SM_Radio_view_0_before.mp4",
    after: "assets/media/dataset/add_bedroom_21_task_0010_add_12_SM_Radio_view_0_after.mp4",
    sourceModel: "assets/models/dataset/add_bedroom_21_task_0010_add_12_SM_Radio_view_0_before.glb",
    editedModel: "assets/models/dataset/add_bedroom_21_task_0010_add_12_SM_Radio_view_0_after.glb",
    thumb: "assets/thumbs/dataset/add_bedroom_21_task_0010_add_12_SM_Radio_view_0_thumb.jpg",
    promptFrame: "assets/thumbs/dataset/add_bedroom_21_task_0010_add_12_SM_Radio_view_0_prompt_frame.jpg",
    usedFixMask: false,
    cameraOrbit: "16.2deg 88.0deg auto"
  },
  {
    id: "add_livingroom_05_task_0004_add_16_SM_Decor_4_view_0",
    label: "Add",
    title: "Add in Livingroom 05",
    prompt: "Add a silver abstract metal sculpture on the wooden TV stand, placing it between the small potted plant and the wooden angel figurine.",
    before: "assets/media/dataset/add_livingroom_05_task_0004_add_16_SM_Decor_4_view_0_before.mp4",
    after: "assets/media/dataset/add_livingroom_05_task_0004_add_16_SM_Decor_4_view_0_after.mp4",
    sourceModel: "assets/models/dataset/add_livingroom_05_task_0004_add_16_SM_Decor_4_view_0_before.glb",
    editedModel: "assets/models/dataset/add_livingroom_05_task_0004_add_16_SM_Decor_4_view_0_after.glb",
    thumb: "assets/thumbs/dataset/add_livingroom_05_task_0004_add_16_SM_Decor_4_view_0_thumb.jpg",
    promptFrame: "assets/thumbs/dataset/add_livingroom_05_task_0004_add_16_SM_Decor_4_view_0_prompt_frame.jpg",
    usedFixMask: false,
    cameraOrbit: "14.0deg 88.0deg auto"
  },
  {
    id: "delete_supermarket_04_task_0003_delete_44_sk20_MR01_view_2",
    label: "Removal",
    title: "Removal in Supermarket 04",
    prompt: "Remove the computer monitor displaying a colorful abstract wallpaper from the wooden desk, leaving the black speaker and keyboard visible.",
    before: "assets/media/dataset/delete_supermarket_04_task_0003_delete_44_sk20_MR01_view_2_before.mp4",
    after: "assets/media/dataset/delete_supermarket_04_task_0003_delete_44_sk20_MR01_view_2_after.mp4",
    sourceModel: "assets/models/dataset/delete_supermarket_04_task_0003_delete_44_sk20_MR01_view_2_before.glb",
    editedModel: "assets/models/dataset/delete_supermarket_04_task_0003_delete_44_sk20_MR01_view_2_after.glb",
    thumb: "assets/thumbs/dataset/delete_supermarket_04_task_0003_delete_44_sk20_MR01_view_2_thumb.jpg",
    promptFrame: "assets/thumbs/dataset/delete_supermarket_04_task_0003_delete_44_sk20_MR01_view_2_prompt_frame.jpg",
    usedFixMask: false,
    cameraOrbit: "6.8deg 88.0deg auto"
  },
  {
    id: "delete_streelitter_01_task_0001_delete_a_SM_Trash_Separated_g3_001_view_0",
    label: "Removal",
    title: "Removal in Streelitter 01",
    prompt: "Remove the dark grey trash bag located on the ground between the other black bags and the white bag near the metal dumpster.",
    before: "assets/media/dataset/delete_streelitter_01_task_0001_delete_a_SM_Trash_Separated_g3_001_view_0_before.mp4",
    after: "assets/media/dataset/delete_streelitter_01_task_0001_delete_a_SM_Trash_Separated_g3_001_view_0_after.mp4",
    sourceModel: "assets/models/dataset/delete_streelitter_01_task_0001_delete_a_SM_Trash_Separated_g3_001_view_0_before.glb",
    editedModel: "assets/models/dataset/delete_streelitter_01_task_0001_delete_a_SM_Trash_Separated_g3_001_view_0_after.glb",
    thumb: "assets/thumbs/dataset/delete_streelitter_01_task_0001_delete_a_SM_Trash_Separated_g3_001_view_0_thumb.jpg",
    promptFrame: "assets/thumbs/dataset/delete_streelitter_01_task_0001_delete_a_SM_Trash_Separated_g3_001_view_0_prompt_frame.jpg",
    usedFixMask: false,
    cameraOrbit: "10.3deg 84.5deg auto"
  },
  {
    id: "delete_official_01_task_0002_delete_7_SM_Trashbin_Trashbin_Small_InsideBody_001_view_1",
    label: "Removal",
    title: "Removal in Official 01",
    prompt: "Remove the black trash bin from the center of the wooden floor, leaving the space between the white chairs and sofa empty.",
    before: "assets/media/dataset/delete_official_01_task_0002_delete_7_SM_Trashbin_Trashbin_Small_InsideBody_001_view_1_before.mp4",
    after: "assets/media/dataset/delete_official_01_task_0002_delete_7_SM_Trashbin_Trashbin_Small_InsideBody_001_view_1_after.mp4",
    sourceModel: "assets/models/dataset/delete_official_01_task_0002_delete_7_SM_Trashbin_Trashbin_Small_InsideBody_001_view_1_before.glb",
    editedModel: "assets/models/dataset/delete_official_01_task_0002_delete_7_SM_Trashbin_Trashbin_Small_InsideBody_001_view_1_after.glb",
    thumb: "assets/thumbs/dataset/delete_official_01_task_0002_delete_7_SM_Trashbin_Trashbin_Small_InsideBody_001_view_1_thumb.jpg",
    promptFrame: "assets/thumbs/dataset/delete_official_01_task_0002_delete_7_SM_Trashbin_Trashbin_Small_InsideBody_001_view_1_prompt_frame.jpg",
    usedFixMask: false,
    cameraOrbit: "-10.3deg 88.0deg auto"
  },
  {
    id: "move_storge_01_task_0008_move_44_sk10_Ladder01_view_0",
    label: "Move",
    title: "Move in Storge 01",
    prompt: "Move the silver metal ladder from the foreground to the back corner of the room, placing it next to the blue water jug and cardboard boxes.",
    before: "assets/media/dataset/move_storge_01_task_0008_move_44_sk10_Ladder01_view_0_before.mp4",
    after: "assets/media/dataset/move_storge_01_task_0008_move_44_sk10_Ladder01_view_0_after.mp4",
    sourceModel: "assets/models/dataset/move_storge_01_task_0008_move_44_sk10_Ladder01_view_0_before.glb",
    editedModel: "assets/models/dataset/move_storge_01_task_0008_move_44_sk10_Ladder01_view_0_after.glb",
    thumb: "assets/thumbs/dataset/move_storge_01_task_0008_move_44_sk10_Ladder01_view_0_thumb.jpg",
    promptFrame: "assets/thumbs/dataset/move_storge_01_task_0008_move_44_sk10_Ladder01_view_0_prompt_frame.jpg",
    usedFixMask: false,
    cameraOrbit: "16.3deg 88.0deg auto"
  },
  {
    id: "move_musicstudio_01_task_0008_move_c_SM_Chair_2_view_3",
    label: "Move",
    title: "Move in Musicstudio 01",
    prompt: "Move the white armchair from the left side of the room to the right side, placing it next to the drum set and cymbal stand.",
    before: "assets/media/dataset/move_musicstudio_01_task_0008_move_c_SM_Chair_2_view_3_before.mp4",
    after: "assets/media/dataset/move_musicstudio_01_task_0008_move_c_SM_Chair_2_view_3_after.mp4",
    sourceModel: "assets/models/dataset/move_musicstudio_01_task_0008_move_c_SM_Chair_2_view_3_before.glb",
    editedModel: "assets/models/dataset/move_musicstudio_01_task_0008_move_c_SM_Chair_2_view_3_after.glb",
    thumb: "assets/thumbs/dataset/move_musicstudio_01_task_0008_move_c_SM_Chair_2_view_3_thumb.jpg",
    promptFrame: "assets/thumbs/dataset/move_musicstudio_01_task_0008_move_c_SM_Chair_2_view_3_prompt_frame.jpg",
    usedFixMask: false,
    cameraOrbit: "-5.6deg 88.0deg auto"
  },
  {
    id: "move_livingroom_16_task_0008_move_0_SM_Stool003_view_0",
    label: "Move",
    title: "Move in Livingroom 16",
    prompt: "Move the gray cylindrical ottoman from the rug onto the wooden floor, positioning it near the corner of the room away from the patterned rug.",
    before: "assets/media/dataset/move_livingroom_16_task_0008_move_0_SM_Stool003_view_0_before.mp4",
    after: "assets/media/dataset/move_livingroom_16_task_0008_move_0_SM_Stool003_view_0_after.mp4",
    sourceModel: "assets/models/dataset/move_livingroom_16_task_0008_move_0_SM_Stool003_view_0_before.glb",
    editedModel: "assets/models/dataset/move_livingroom_16_task_0008_move_0_SM_Stool003_view_0_after.glb",
    thumb: "assets/thumbs/dataset/move_livingroom_16_task_0008_move_0_SM_Stool003_view_0_thumb.jpg",
    promptFrame: "assets/thumbs/dataset/move_livingroom_16_task_0008_move_0_SM_Stool003_view_0_prompt_frame.jpg",
    usedFixMask: false,
    cameraOrbit: "12.2deg 88.0deg auto"
  },
  {
    id: "mix_livingroom_10_task_0010_add_delete_mix_20_SM_Bowl_with_Oranges_x_12_SM_Radio_view_0",
    label: "Mixed",
    title: "Mixed in Livingroom 10",
    prompt: "Add a bowl of bright orange fruits onto the front-left wooden coffee table, and remove the blue vintage radio from the lower cubby of the wooden bookcase.",
    before: "assets/media/dataset/mix_livingroom_10_task_0010_add_delete_mix_20_SM_Bowl_with_Oranges_x_12_SM_Radio_view_0_before.mp4",
    after: "assets/media/dataset/mix_livingroom_10_task_0010_add_delete_mix_20_SM_Bowl_with_Oranges_x_12_SM_Radio_view_0_after.mp4",
    sourceModel: "assets/models/dataset/mix_livingroom_10_task_0010_add_delete_mix_20_SM_Bowl_with_Oranges_x_12_SM_Radio_view_0_before.glb",
    editedModel: "assets/models/dataset/mix_livingroom_10_task_0010_add_delete_mix_20_SM_Bowl_with_Oranges_x_12_SM_Radio_view_0_after.glb",
    thumb: "assets/thumbs/dataset/mix_livingroom_10_task_0010_add_delete_mix_20_SM_Bowl_with_Oranges_x_12_SM_Radio_view_0_thumb.jpg",
    promptFrame: "assets/thumbs/dataset/mix_livingroom_10_task_0010_add_delete_mix_20_SM_Bowl_with_Oranges_x_12_SM_Radio_view_0_prompt_frame.jpg",
    usedFixMask: false,
    cameraOrbit: "-11.1deg 88.0deg auto"
  },
  {
    id: "mix_streelitter_06_task_0010_add_delete_mix_a_Ladder_x_a_SM_Ammo_Box_Green_Wood_view_1",
    label: "Mixed",
    title: "Mixed in Streelitter 06",
    prompt: "Remove the green metal military box and blue cooler from the roof of the light blue van, and add a white folding ladder leaning against the side of the vehicle.",
    before: "assets/media/dataset/mix_streelitter_06_task_0010_add_delete_mix_a_Ladder_x_a_SM_Ammo_Box_Green_Wood_view_1_before.mp4",
    after: "assets/media/dataset/mix_streelitter_06_task_0010_add_delete_mix_a_Ladder_x_a_SM_Ammo_Box_Green_Wood_view_1_after.mp4",
    sourceModel: "assets/models/dataset/mix_streelitter_06_task_0010_add_delete_mix_a_Ladder_x_a_SM_Ammo_Box_Green_Wood_view_1_before.glb",
    editedModel: "assets/models/dataset/mix_streelitter_06_task_0010_add_delete_mix_a_Ladder_x_a_SM_Ammo_Box_Green_Wood_view_1_after.glb",
    thumb: "assets/thumbs/dataset/mix_streelitter_06_task_0010_add_delete_mix_a_Ladder_x_a_SM_Ammo_Box_Green_Wood_view_1_thumb.jpg",
    promptFrame: "assets/thumbs/dataset/mix_streelitter_06_task_0010_add_delete_mix_a_Ladder_x_a_SM_Ammo_Box_Green_Wood_view_1_prompt_frame.jpg",
    usedFixMask: false,
    cameraOrbit: "-15.4deg 88.0deg auto"
  }
];

const DEFAULT_COMPARE_CASE_ID = "scannetpp_case_10000_40step_0006_original_f024";
const DATASET_CAROUSEL_OFFSETS = [-2, -1, 0, 1, 2];
const MODEL_CAMERA_ORBIT_FALLBACK = "0deg 82deg auto";
const MODEL_CAMERA_RADIUS = "86%";
const MODEL_ASSET_BASE_URL = (window.JOINTEDIT3D_MODEL_BASE_URL || "").replace(/\/$/, "");

document.addEventListener("DOMContentLoaded", () => {
  initComparisons();
  initDatasetSamples();
  initAdditionalResultsCarousel();
});

function initComparisons() {
  const container = document.querySelector("#comparison-grid");

  if (!container) {
    return;
  }

  const defaultIndex = Math.max(0, COMPARE_CASES.findIndex((item) => item.id === DEFAULT_COMPARE_CASE_ID));
  let activeIndex = defaultIndex;
  const stage = document.createElement("div");
  const carousel = document.createElement("div");
  const track = document.createElement("div");
  const prevButton = createSampleCarouselButton("prev", "Previous inference example");
  const nextButton = createSampleCarouselButton("next", "Next inference example");
  stage.className = "inference-sample-stage";
  carousel.className = "dataset-sample-tabs inference-sample-tabs";
  carousel.setAttribute("aria-label", "Inference example cases");
  track.className = "dataset-sample-track inference-sample-track";
  track.setAttribute("role", "list");
  carousel.append(prevButton, track, nextButton);
  container.replaceChildren(stage, carousel);

  prevButton.addEventListener("click", () => renderSample(activeIndex - 1, true, true));
  nextButton.addEventListener("click", () => renderSample(activeIndex + 1, true, true));

  function renderCarousel(direction = 0) {
    const fragment = document.createDocumentFragment();

    DATASET_CAROUSEL_OFFSETS.forEach((offset, motionIndex) => {
      const sampleIndex = wrapIndex(activeIndex + offset, COMPARE_CASES.length);
      const item = COMPARE_CASES[sampleIndex];
      const isActive = offset === 0;
      const button = createSampleThumb(item, {
        image: inferenceThumb(item),
        showLabel: false,
        extraClass: "dataset-sample-thumb inference-sample-thumb"
      });
      button.setAttribute("role", "listitem");
      button.setAttribute("aria-label", `Show ${item.title}`);
      button.setAttribute("aria-current", isActive ? "true" : "false");
      button.setAttribute("aria-pressed", String(isActive));
      button.style.setProperty("--motion-index", String(motionIndex));
      button.classList.toggle("active", isActive);
      button.addEventListener("click", () => {
        if (!isActive) {
          renderSample(sampleIndex, true, true);
        }
      });
      fragment.appendChild(button);
    });

    track.replaceChildren(fragment);
    animateSampleTrack(track, direction);
  }

  function renderSample(index, shouldAnimate = true, loadMedia = true) {
    const previousIndex = activeIndex;
    activeIndex = wrapIndex(index, COMPARE_CASES.length);
    const direction = shouldAnimate ? sampleMotionDirection(previousIndex, activeIndex, COMPARE_CASES.length) : 0;
    renderCarousel(direction);
    disposeMedia(stage);
    stage.replaceChildren(createCompareCard(COMPARE_CASES[activeIndex], loadMedia));
    if (direction !== 0) {
      animateSampleStage(stage, direction);
    }
  }

  renderSample(defaultIndex, false, true);
}

function createCompareCard(item, loadMedia = true) {
  const card = document.createElement("article");
  card.className = "compare-card paired-inference-card";

  const body = document.createElement("div");
  body.className = "paired-inference-body";

  const comparePanel = document.createElement("div");
  comparePanel.className = "paired-inference-panel";
  const compareHeading = document.createElement("h4");
  compareHeading.textContent = "Paired RGB edit";
  let compareNode;
  compareNode = loadMedia ? createCompareStage(item, { showTag: false }) : createLazyMediaCard({
    type: "video",
    label: item.label,
    image: inferenceThumb(item),
    alt: `${item.title} preview frame`,
    onLoad: () => {
      if (!compareNode.isConnected) {
        return;
      }
      compareNode.replaceWith(createCompareStage(item, { showTag: false }));
    }
  });
  comparePanel.append(compareHeading, compareNode);

  const modelPanel = document.createElement("div");
  modelPanel.className = "paired-inference-panel";
  const modelHeading = document.createElement("h4");
  modelHeading.textContent = "3D preview";
  let modelNode;
  modelNode = loadMedia ? createModelViewerCard({
    label: item.modelLabel,
    url: item.model,
    alt: `${item.title} 3D preview`,
    cameraOrbit: item.cameraOrbit,
    orientation: item.modelOrientation,
    mirrorCameraTheta: item.mirrorCameraTheta
  }, {
    loading: "eager",
    reveal: "auto"
  }) : createLazyMediaCard({
    type: "3d",
    label: item.modelLabel,
    image: inferenceThumb(item),
    alt: `${item.title} 3D preview poster`,
    onLoad: () => {
      if (!modelNode.isConnected) {
        return;
      }
      modelNode.replaceWith(createModelViewerCard({
        label: item.modelLabel,
        url: item.model,
        alt: `${item.title} 3D preview`,
        cameraOrbit: item.cameraOrbit,
        orientation: item.modelOrientation,
        mirrorCameraTheta: item.mirrorCameraTheta
      }, {
        loading: "eager",
        reveal: "auto"
      }));
    }
  });
  modelPanel.append(modelHeading, modelNode);

  body.append(comparePanel, modelPanel);
  card.append(body);

  return card;
}

function inferenceThumb(item) {
  return `assets/thumbs/inference/${item.id}_thumb.jpg`;
}

function createCompareStage(item, options = {}) {
  const stage = document.createElement("div");
  stage.className = "compare-stage";

  const beforeLayer = document.createElement("div");
  beforeLayer.className = "compare-layer before";
  beforeLayer.appendChild(createMedia(item.before, `${item.title} before`));

  const afterLayer = document.createElement("div");
  afterLayer.className = "compare-layer after";
  afterLayer.appendChild(createMedia(item.after, `${item.title} after`));

  const beforeLabel = document.createElement("span");
  beforeLabel.className = "compare-label before";
  beforeLabel.textContent = item.beforeLabel;

  const afterLabel = document.createElement("span");
  afterLabel.className = "compare-label after";
  afterLabel.textContent = item.afterLabel;

  const divider = document.createElement("div");
  divider.className = "compare-divider";

  const handle = document.createElement("div");
  handle.className = "compare-handle";
  divider.appendChild(handle);

  const range = document.createElement("input");
  range.className = "compare-range";
  range.type = "range";
  range.min = "0";
  range.max = "100";
  range.value = "50";
  range.setAttribute("aria-label", `${item.title} before after divider`);

  const videos = [];
  beforeLayer.querySelectorAll("video").forEach((video) => videos.push(video));
  afterLayer.querySelectorAll("video").forEach((video) => videos.push(video));

  range.addEventListener("input", () => updateDivider(range.value, afterLayer, divider));
  stage.append(beforeLayer, afterLayer, beforeLabel, afterLabel, divider, range);
  if (options.showTag !== false) {
    const tag = document.createElement("span");
    tag.className = "demo-tag";
    tag.textContent = item.label;
    stage.appendChild(tag);
  }
  updateDivider(50, afterLayer, divider);

  if (videos.length > 0) {
    stage.appendChild(createVideoToggle(videos));
    syncVideos(videos);
  }

  return stage;
}

function createMedia(source, alt) {
  const isVideo = /\.(mp4|webm|mov)(\?.*)?$/i.test(source);
  if (isVideo) {
    const video = document.createElement("video");
    video.className = "compare-media";
    video.src = source;
    video.muted = true;
    video.loop = true;
    video.autoplay = true;
    video.playsInline = true;
    video.preload = "metadata";
    video.setAttribute("aria-label", alt);
    video.addEventListener("canplay", () => {
      video.play().catch(() => {});
    }, { once: true });
    return video;
  }

  const image = document.createElement("img");
  image.className = "compare-media";
  image.src = source;
  image.alt = alt;
  image.loading = "lazy";
  return image;
}

function disposeMedia(root) {
  if (!root) {
    return;
  }

  root.querySelectorAll("video").forEach((video) => {
    video.pause();
    video.removeAttribute("src");
    video.load();
  });

  root.querySelectorAll("model-viewer").forEach((viewer) => {
    viewer.removeAttribute("src");
  });
}

function updateDivider(value, afterLayer, divider) {
  const percent = Number(value);
  afterLayer.style.clipPath = `inset(0 ${100 - percent}% 0 0)`;
  divider.style.left = `${percent}%`;
}

function createVideoToggle(videos) {
  let playing = true;
  const button = document.createElement("button");
  const icon = document.createElement("span");
  button.type = "button";
  button.className = "icon-button video-toggle active";
  button.setAttribute("aria-label", "Pause videos");
  icon.className = "icon-pause";
  icon.setAttribute("aria-hidden", "true");
  button.appendChild(icon);

  button.addEventListener("click", () => {
    playing = !playing;
    videos.forEach((video) => {
      if (playing) {
        video.play().catch(() => {});
      } else {
        video.pause();
      }
    });
    button.classList.toggle("active", playing);
    button.setAttribute("aria-label", playing ? "Pause videos" : "Play videos");
    icon.className = playing ? "icon-pause" : "icon-play";
  });

  return button;
}

function syncVideos(videos) {
  if (videos.length < 2) {
    return;
  }

  const leader = videos[0];
  videos.forEach((video) => {
    video.addEventListener("loadedmetadata", () => {
      if (video !== leader && Number.isFinite(leader.currentTime)) {
        video.currentTime = leader.currentTime;
      }
    });
  });

  leader.addEventListener("timeupdate", () => {
    videos.slice(1).forEach((video) => {
      if (!Number.isFinite(video.duration) || video.duration <= 0) {
        return;
      }
      const target = leader.currentTime % video.duration;
      if (Math.abs(video.currentTime - target) > 0.08) {
        video.currentTime = target;
      }
    });
  });
}

function initDatasetSamples() {
  const stage = document.querySelector("#dataset-sample-stage");
  const carousel = document.querySelector("#dataset-sample-tabs");

  if (!stage || !carousel) {
    return;
  }

  let activeIndex = 0;
  const track = document.createElement("div");
  const prevButton = createSampleCarouselButton("prev", "Previous dataset sample");
  const nextButton = createSampleCarouselButton("next", "Next dataset sample");
  track.className = "dataset-sample-track";
  track.setAttribute("role", "list");
  carousel.replaceChildren(prevButton, track, nextButton);

  prevButton.addEventListener("click", () => renderSample(activeIndex - 1, true, true));
  nextButton.addEventListener("click", () => renderSample(activeIndex + 1, true, true));

  function renderCarousel(direction = 0) {
    const fragment = document.createDocumentFragment();

    DATASET_CAROUSEL_OFFSETS.forEach((offset, motionIndex) => {
      const sampleIndex = wrapIndex(activeIndex + offset, DATASET_SAMPLES.length);
      const item = DATASET_SAMPLES[sampleIndex];
      const isActive = offset === 0;
      const button = createSampleThumb(item, {
        image: item.thumb,
        showLabel: false,
        extraClass: "dataset-sample-thumb"
      });
      button.setAttribute("role", "listitem");
      button.setAttribute("aria-label", `Show ${item.title}`);
      button.setAttribute("aria-current", isActive ? "true" : "false");
      button.setAttribute("aria-pressed", String(isActive));
      button.style.setProperty("--motion-index", String(motionIndex));
      button.classList.toggle("active", isActive);
      button.addEventListener("click", () => {
        if (!isActive) {
          renderSample(sampleIndex, true, true);
        }
      });
      fragment.appendChild(button);
    });

    track.replaceChildren(fragment);
    animateSampleTrack(track, direction);
  }

  function renderSample(index, shouldScroll = true, loadMedia = true) {
    const previousIndex = activeIndex;
    activeIndex = wrapIndex(index, DATASET_SAMPLES.length);
    const direction = shouldScroll ? sampleMotionDirection(previousIndex, activeIndex, DATASET_SAMPLES.length) : 0;
    renderCarousel(direction);
    const item = DATASET_SAMPLES[activeIndex];

    const comparePanel = document.createElement("article");
    comparePanel.className = "dataset-sample-panel";
    const compareTitle = document.createElement("h4");
    compareTitle.textContent = "Paired RGB edit";
    const compareItem = {
      id: item.id,
      label: item.label,
      title: item.title,
      before: item.before,
      after: item.after,
      beforeLabel: "Source",
      afterLabel: "Edited"
    };
    let compareNode;
    compareNode = loadMedia ? createCompareStage(compareItem) : createLazyMediaCard({
        type: "video",
        label: item.label,
        image: item.thumb,
        alt: `${item.title} preview frame`,
        onLoad: () => {
          compareNode.replaceWith(createCompareStage(compareItem));
        }
      });
    comparePanel.append(compareTitle, compareNode);

    const promptPanel = document.createElement("article");
    promptPanel.className = "dataset-sample-panel prompt-panel";
    const promptTitle = document.createElement("h4");
    promptTitle.textContent = "Edit prompt";
    promptPanel.append(promptTitle, createPromptCard(item));

    const modelPanel = document.createElement("article");
    modelPanel.className = "dataset-sample-panel";
    const modelTitle = document.createElement("h4");
    modelTitle.textContent = "Paired 3D preview";
    modelPanel.append(modelTitle, createModelSwitcher(item, loadMedia));

    stage.replaceChildren(comparePanel, promptPanel, modelPanel);
    if (direction !== 0) {
      animateSampleStage(stage, direction);
    }
  }

  renderSample(0, false, false);
}

function createSampleCarouselButton(direction, label) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = `sample-carousel-button ${direction}`;
  button.setAttribute("aria-label", label);

  const icon = document.createElement("span");
  icon.className = `sample-carousel-arrow ${direction}`;
  icon.setAttribute("aria-hidden", "true");
  button.appendChild(icon);

  return button;
}

function wrapIndex(index, length) {
  return ((index % length) + length) % length;
}

function sampleMotionDirection(previousIndex, nextIndex, length) {
  if (previousIndex === nextIndex || length <= 1) {
    return 0;
  }
  const forward = wrapIndex(nextIndex - previousIndex, length);
  const backward = wrapIndex(previousIndex - nextIndex, length);
  return forward <= backward ? 1 : -1;
}

function prefersReducedMotion() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

function animateSampleTrack(track, direction) {
  if (!direction || prefersReducedMotion()) {
    return;
  }

  track.classList.remove("slide-next", "slide-prev");
  void track.offsetWidth;
  track.classList.add(direction > 0 ? "slide-next" : "slide-prev");
  window.setTimeout(() => {
    track.classList.remove("slide-next", "slide-prev");
  }, 360);

  if (typeof track.animate !== "function") {
    return;
  }

  const distance = direction > 0 ? 84 : -84;
  track.getAnimations().forEach((animation) => animation.cancel());
  track.animate([
    { transform: `translateX(${distance}px)`, opacity: 0.78 },
    { transform: "translateX(0)", opacity: 1 }
  ], {
    duration: 320,
    easing: "cubic-bezier(0.2, 0.72, 0.18, 1)",
    fill: "both"
  });

  Array.from(track.children).forEach((child, index) => {
    child.animate([
      { transform: "scale(0.96)", opacity: 0.86 },
      { transform: "scale(1)", opacity: 1 }
    ], {
      duration: 260,
      delay: index * 18,
      easing: "cubic-bezier(0.2, 0.72, 0.18, 1)",
      fill: "both"
    });
  });
}

function animateSampleStage(stage, direction) {
  if (!direction || prefersReducedMotion() || typeof stage.animate !== "function") {
    return;
  }

  const distance = direction > 0 ? 18 : -18;
  stage.getAnimations().forEach((animation) => animation.cancel());
  stage.animate([
    { transform: `translateX(${distance}px)`, opacity: 0.88 },
    { transform: "translateX(0)", opacity: 1 }
  ], {
    duration: 240,
    easing: "cubic-bezier(0.2, 0.72, 0.18, 1)",
    fill: "both"
  });
}

function createPromptCard(item) {
  const card = document.createElement("div");
  card.className = "prompt-card";

  const badge = document.createElement("span");
  badge.className = "prompt-badge";
  badge.textContent = item.label;

  const prompt = document.createElement("p");
  prompt.textContent = item.prompt;

  card.append(badge, prompt);
  return card;
}

function createModelSwitcher(item, loadMedia) {
  const wrapper = document.createElement("div");
  wrapper.className = "model-switcher";

  const controls = document.createElement("div");
  controls.className = "model-switcher-tabs";

  const viewerSlot = document.createElement("div");
  viewerSlot.className = "model-switcher-slot";

  const options = [
    { key: "source", label: "Source", url: item.sourceModel, cameraOrbit: item.cameraOrbit },
    { key: "edited", label: "Edited", url: item.editedModel, cameraOrbit: item.cameraOrbit }
  ];

  function activate(activeKey) {
    Array.from(controls.children).forEach((button) => {
      const isActive = button.dataset.key === activeKey;
      button.classList.toggle("active", isActive);
      button.setAttribute("aria-pressed", String(isActive));
    });

    const option = options.find((candidate) => candidate.key === activeKey) || options[0];
    const card = loadMedia ? createModelViewerCard({
      label: `${option.label} 3D`,
      url: option.url,
      alt: `${item.title} ${option.label.toLowerCase()} 3D preview`,
      cameraOrbit: option.cameraOrbit
    }, {
      loading: "eager",
      reveal: "auto"
    }) : createLazyMediaCard({
      type: "3d",
      label: `${option.label} 3D`,
      image: item.thumb,
      alt: `${item.title} ${option.label.toLowerCase()} 3D preview poster`,
      onLoad: () => {
        loadMedia = true;
        activate(activeKey);
      }
    });
    viewerSlot.replaceChildren(card);
  }

  options.forEach((option) => {
    const button = document.createElement("button");
    button.type = "button";
    button.dataset.key = option.key;
    button.textContent = option.label;
    button.addEventListener("click", () => activate(option.key));
    controls.appendChild(button);
  });

  wrapper.append(controls, viewerSlot);
  activate("edited");
  return wrapper;
}

function createLazyMediaCard(item) {
  const card = document.createElement("div");
  card.className = `lazy-media-card kind-${item.type}`;

  const image = document.createElement("img");
  image.src = item.image;
  image.alt = item.alt;
  image.loading = "lazy";

  const badge = document.createElement("span");
  badge.className = "lazy-media-badge";
  badge.textContent = item.label;

  card.append(image, badge);
  observeAutoLoad(card, item.onLoad);
  return card;
}

function observeAutoLoad(element, onLoad) {
  let loaded = false;
  const load = () => {
    if (loaded) {
      return;
    }
    loaded = true;
    onLoad();
  };

  if (!("IntersectionObserver" in window)) {
    window.requestAnimationFrame(load);
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    if (entries.some((entry) => entry.isIntersecting)) {
      observer.disconnect();
      load();
    }
  }, {
    rootMargin: "160px 0px",
    threshold: 0.18
  });

  observer.observe(element);
}

function createSampleThumb(item, options = {}) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = `cloud-thumb${options.extraClass ? ` ${options.extraClass}` : ""}`;
  if (item.id) {
    button.dataset.id = item.id;
  }

  const image = document.createElement("img");
  image.src = options.image || item.thumb;
  image.alt = "";
  image.loading = "lazy";

  button.appendChild(image);

  if (options.showLabel !== false) {
    const label = document.createElement("span");
    label.textContent = item.title || item.label;
    button.appendChild(label);
  }

  return button;
}

function createModelViewerCard(item, options = {}) {
  const element = document.createElement("article");
  element.className = "cloud-card model-viewer-card";

  const label = document.createElement("span");
  label.className = "cloud-label";
  label.textContent = item.label;

  const viewer = document.createElement("model-viewer");
  viewer.setAttribute("src", resolveModelUrl(item.url));
  viewer.setAttribute("alt", item.alt);
  viewer.setAttribute("camera-controls", "");
  viewer.setAttribute("camera-target", "0m 0m 0m");
  viewer.setAttribute("camera-orbit", createCloserCameraOrbit(item.cameraOrbit, item.mirrorCameraTheta));
  if (item.orientation) {
    viewer.setAttribute("orientation", item.orientation);
  }
  viewer.setAttribute("disable-tap", "");
  viewer.setAttribute("environment-image", "legacy");
  viewer.setAttribute("interaction-prompt", "none");
  viewer.setAttribute("loading", options.loading || "lazy");
  const reveal = options.reveal === undefined ? "interaction" : options.reveal;
  if (reveal) {
    viewer.setAttribute("reveal", reveal);
  }
  viewer.setAttribute("max-camera-orbit", "auto auto 10m");
  viewer.setAttribute("min-camera-orbit", "auto auto 1m");
  viewer.setAttribute("shadow-intensity", "0");
  viewer.setAttribute("touch-action", "pan-y");
  viewer.setAttribute("zoom-sensitivity", "0.2");

  const hint = document.createElement("span");
  hint.className = "cloud-hint";
  hint.textContent = "drag";

  element.append(label, viewer, hint);
  return element;
}

function resolveModelUrl(url) {
  if (!MODEL_ASSET_BASE_URL || /^https?:\/\//i.test(url)) {
    return url;
  }
  return url.replace(/^assets\/models/, MODEL_ASSET_BASE_URL);
}

function createCloserCameraOrbit(cameraOrbit, mirrorTheta = false) {
  const orbit = cameraOrbit || MODEL_CAMERA_ORBIT_FALLBACK;
  const radiusAdjusted = orbit.replace(/\s+auto\s*$/, ` ${MODEL_CAMERA_RADIUS}`);
  if (!mirrorTheta) {
    return radiusAdjusted;
  }
  return radiusAdjusted.replace(/^(-?\d+(?:\.\d+)?)deg\b/, (_, theta) => `${-Number(theta)}deg`);
}

function initAdditionalResultsCarousel() {
  const carousel = document.querySelector("[data-carousel]");

  if (!carousel) {
    return;
  }

  const track = carousel.querySelector(".results-carousel-track");
  const slides = Array.from(carousel.querySelectorAll(".carousel-slide"));
  const dotsWrap = carousel.querySelector("#additional-results-dots");
  const prev = carousel.querySelector("[data-carousel-prev]");
  const next = carousel.querySelector("[data-carousel-next]");

  if (!track || slides.length === 0 || !dotsWrap) {
    return;
  }

  const dots = slides.map((slide, index) => {
    const dot = document.createElement("button");
    dot.type = "button";
    dot.className = "carousel-dot";
    dot.setAttribute("aria-label", `Show result ${index + 1}`);
    dot.addEventListener("click", () => goToSlide(index));
    dotsWrap.appendChild(dot);
    return dot;
  });

  function getSlideWidth() {
    return slides[0].getBoundingClientRect().width || track.getBoundingClientRect().width;
  }

  function currentIndex() {
    const width = getSlideWidth();
    if (!width) {
      return 0;
    }
    return Math.max(0, Math.min(slides.length - 1, Math.round(track.scrollLeft / width)));
  }

  function updateState() {
    const active = currentIndex();
    dots.forEach((dot, index) => {
      const isActive = index === active;
      dot.classList.toggle("active", isActive);
      dot.setAttribute("aria-current", isActive ? "true" : "false");
    });
  }

  function goToSlide(index) {
    const target = Math.max(0, Math.min(slides.length - 1, index));
    track.scrollTo({
      left: getSlideWidth() * target,
      behavior: "smooth"
    });
  }

  prev?.addEventListener("click", () => goToSlide(currentIndex() - 1));
  next?.addEventListener("click", () => goToSlide(currentIndex() + 1));
  track.addEventListener("scroll", () => {
    window.requestAnimationFrame(updateState);
  });
  window.addEventListener("resize", () => goToSlide(currentIndex()));
  updateState();
}
