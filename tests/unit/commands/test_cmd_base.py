from unittest.mock import AsyncMock, MagicMock, call

import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "all_models, args_models, exp_models",
    [
        ([], ["test-model"], []),
        (["model1", "model2", "model3"], ["test-model"], []),
        (["model1", "model2", "model3"], ["model1"], ["model1"]),
        (["model1", "model2", "model3"], ["model1", "model2"], ["model1", "model2"]),
        (["model1", "model2", "model3"], [], ["model1", "model2", "model3"]),
        (["model1", "model2", "model3"], None, ["model1", "model2", "model3"]),
    ],
)
async def test_get_filtered_models(
    all_models, args_models, exp_models, test_juju_command
):
    """Test async models generator."""
    mock_controller = AsyncMock()
    mock_controller.get_models.return_value = all_models
    mock_controller.get_model.return_value = mock_model = AsyncMock()

    models_generator = test_juju_command.get_filtered_models(
        mock_controller, args_models
    )
    models = [name async for name, _ in models_generator]

    # check returned models
    assert models == exp_models
    # check that model was get from controller
    mock_controller.get_model.assert_has_awaits(calls=[call(name) for name in models])
    # check that model was disconnected
    assert mock_model.disconnect.await_count == len(models)


@pytest.mark.asyncio
async def test_run(test_juju_command):
    """Test run for any juju command."""
    mock_controller = MagicMock()

    await test_juju_command.run(mock_controller, test=5)

    test_juju_command.execute.assert_called_once_with(mock_controller, test=5)


def test_need_shuttle(test_juju_command):
    """Test default return value for need_shuttle property."""
    assert test_juju_command.need_sshuttle is False
